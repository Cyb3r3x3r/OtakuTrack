import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def scrape_anime_list(query):
    # First try Jikan API (multiple results)
    jikan_results = search_anime_jikan_all(query)
    if jikan_results:
        return jikan_results

    # Fallback to BS4 (single result)
    bs4_result = search_anime_bs4(query)
    return [bs4_result] if bs4_result else []


def search_anime_jikan_all(query):
    try:
        url = f"https://api.jikan.moe/v4/anime?q={query}&limit=10"
        res = requests.get(url, headers=HEADERS).json()

        results = []
        for anime in res.get('data', []):
            results.append({
                "title": anime.get('title'),
                "episodes": anime.get('episodes', 'Unknown'),
                "status": anime.get('status', 'Unknown'),
                "rating": anime.get('score') or None,  # 🆕 Add rating
                "source": "MyAnimeList (Jikan)",
                "link": anime.get('url')
            })
        return results if results else None
    except Exception as e:
        print("Jikan error:", e)
        return None


def search_anime_bs4(query):
    try:
        print(f"Falling back to BS4 for '{query}'...")
        # Google search to find a MyAnimeList or AnimePlanet link
        search_url = f"https://www.google.com/search?q={query}+site:myanimelist.net"
        res = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, 'html.parser')

        link = None
        for a in soup.select('a'):
            href = a.get('href')
            if href and "myanimelist.net/anime/" in href:
                link = href.split('&')[0].replace("/url?q=", "")
                break

        if not link:
            return None

        # Scrape the anime page
        page = requests.get(link, headers=HEADERS)
        soup = BeautifulSoup(page.text, 'html.parser')

        title = soup.find('h1').text.strip()
        episodes = soup.find(text="Episodes:").find_next().text.strip()
        status = soup.find(text="Status:").find_next().text.strip()

        # 🆕 Try to extract rating from MAL page
        rating_tag = soup.find('span', itemprop='ratingValue')
        rating = float(rating_tag.text.strip()) if rating_tag else None

        return {
            "title": title,
            "episodes": episodes,
            "status": status,
            "rating": rating,
            "source": "MyAnimeList (BS4)",
            "link": link
        }

    except Exception as e:
        print("BS4 scraping error:", e)

    return None
