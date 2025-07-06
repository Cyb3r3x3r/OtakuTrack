from flask import Blueprint, render_template,redirect,request,url_for,flash
from flask_login import login_required, current_user
from models import Anime
from app import db
from scraper import scrape_anime_list

anime = Blueprint('anime', __name__)

@anime.route('/dashboard')
@login_required
def dashboard():
    anime_list = (
        Anime.query
        .filter_by(user_id=current_user.id, watch_status="Plan to Watch")
        .order_by(Anime.rating.desc())
        .limit(5)
        .all()
    )

    return render_template('dashboard.html', anime_list=anime_list)

@anime.route('/search', methods=['POST'])
@login_required
def search_anime():
    anime_name = request.form['anime_name']
    return redirect(url_for('anime.search_result', name=anime_name))


#calls Jikan + BS4 scraper
@anime.route('/search_result')
@login_required
def search_result():
    anime_name = request.args.get('name')
    anime_list = scrape_anime_list(anime_name)

    if not anime_list:
        flash("No anime found for that name.", "danger")
        return redirect(url_for('anime.dashboard'))

    return render_template('search_result.html', anime_list=anime_list)


@anime.route('/add_scraped_anime', methods=['POST'])
@login_required
def add_scraped_anime():
    title = request.form['title']
    episodes = request.form['episodes']
    status = request.form['status']
    source = request.form['source']
    watch_status = request.form['watch_status']  # 🆕
    rating = request.form['rating']  # 🆕


    anime = Anime(
        title=title,
        episodes=episodes,
        status=status,
        source=source,
        watch_status=watch_status,
        rating=rating,
        user_id=current_user.id
    )
    db.session.add(anime)
    db.session.commit()

    flash(f"{title} added to your watchlist under '{watch_status}'.", "success")
    return redirect(url_for('anime.dashboard'))

@anime.route('/watchlist')
@login_required
def watchlist():
    page_ptw = request.args.get('ptw_page', 1, type=int)
    page_watching = request.args.get('watching_page', 1, type=int)
    page_completed = request.args.get('completed_page', 1, type=int)
    per_page = 5

    plan_to_watch = Anime.query.filter_by(user_id=current_user.id, watch_status="Plan to Watch")\
        .order_by(Anime.rating.desc())\
        .paginate(page=page_ptw, per_page=per_page, error_out=False)

    watching = Anime.query.filter_by(user_id=current_user.id, watch_status="Watching")\
        .order_by(Anime.title.asc())\
        .paginate(page=page_watching, per_page=per_page, error_out=False)

    completed = Anime.query.filter_by(user_id=current_user.id, watch_status="Completed")\
        .order_by(Anime.title.asc())\
        .paginate(page=page_completed, per_page=per_page, error_out=False)

    return render_template('watchlist.html',
                           plan_to_watch=plan_to_watch,
                           watching=watching,
                           completed=completed)

@anime.route('/update_status/<int:anime_id>', methods=['POST'])
@login_required
def update_status(anime_id):
    new_status = request.form['watch_status']
    anime = Anime.query.get_or_404(anime_id)

    if anime.user_id != current_user.id:
        flash("Unauthorized update attempt!", "danger")
        return redirect(url_for('anime.watchlist'))

    anime.watch_status = new_status
    db.session.commit()
    flash(f"Updated '{anime.title}' to {new_status}.", "success")
    return redirect(url_for('anime.watchlist'))


@anime.route('/delete_anime/<int:anime_id>', methods=['POST'])
@login_required
def delete_anime(anime_id):
    anime = Anime.query.get_or_404(anime_id)

    if anime.user_id != current_user.id:
        flash("Unauthorized delete attempt!", "danger")
        return redirect(url_for('anime.watchlist'))

    db.session.delete(anime)
    db.session.commit()
    flash(f"Deleted '{anime.title}' from your watchlist.", "success")
    return redirect(url_for('anime.watchlist'))