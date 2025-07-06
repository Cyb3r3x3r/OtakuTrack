# 🌸 OtakuTrack - Anime Watchlist Tracker

OtakuTrack is a portfolio-worthy Flask web app that helps anime lovers track their watchlist. It lets users search anime using the Jikan API (MyAnimeList), organize them by status (Watching, Completed, Plan to Watch), and manage them with a beautiful, responsive UI. Built with free and open-source tools — no API keys, no paid services.


---

## 🚀 Features

- 🔍 **Anime Search** using Jikan API + fallback to BeautifulSoup scraping
- 📝 **Three Watchlist Categories**: Watching, Completed, Plan to Watch
- ✅ **User Authentication** (Register/Login with secure sessions)
- ♻️ **Update or Delete** entries anytime
- 🖼️ **Responsive Frontend** with TailwindCSS and custom themes
- 📂 **Pagination** support for large watchlists
- 💾 **SQLite** database — no setup required
- 🌐 **Deployable on Render** (free tier supported)

---

## 🛠️ Tech Stack

| Frontend        | Backend        | Database | Other Tools          |
|-----------------|----------------|----------|-----------------------|
| HTML + Jinja2   | Flask (Python) | SQLite   | BeautifulSoup, Jikan |
| Tailwind CSS    | Flask-Login    | SQLAlchemy | Gunicorn, Render    |

---

## 🔐 Setup & Installation

```bash
git clone https://github.com/Cyb3r3x3r/otakutrack.git
cd otakutrack

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
