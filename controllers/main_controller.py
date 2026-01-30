from flask import Blueprint, render_template, request
from models.models import Album, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    genre_filter = request.args.get('genre')
    sort_year = request.args.get('sort_year')

    query = Album.query

    if genre_filter:
        query = query.filter_by(genre=genre_filter)

    if sort_year == 'asc':
        query = query.order_by(Album.year.asc())
    elif sort_year == 'desc':
        query = query.order_by(Album.year.desc())

    albums = query.all()
    genres = [g[0] for g in db.session.query(Album.genre).distinct().all()]

    return render_template('index.html', albums=albums, genres=genres)