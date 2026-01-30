from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import func
from models.models import Artist, Album, Review, db


main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    sort_method = request.args.get('sort', 'rating_desc') 
    genre_filter = request.args.get('genre')

    artists = Artist.query.all()

    query = db.session.query(Album).outerjoin(Review).group_by(Album.id)

    if genre_filter:
        query = query.filter(Album.genre == genre_filter)

    if sort_method == 'newest':
        query = query.order_by(Album.year.desc())

    elif sort_method == 'oldest':
        query = query.order_by(Album.year.asc())

    elif sort_method == 'rating_desc':
        avg_rating = func.avg(Review.rating)
        query = query.order_by(func.coalesce(avg_rating, 5).desc())

    elif sort_method == 'rating_asc':
        avg_rating = func.avg(Review.rating)
        query = query.order_by(func.coalesce(avg_rating, 5).asc())

    elif sort_method == 'az':
        query = query.order_by(Album.title.asc())

    albums = query.all()

    genres = [g[0] for g in db.session.query(Album.genre).distinct().all() if g[0]]

    return render_template('index.html', artists=artists, albums=albums, genres=genres)


@main_bp.route('/artist/<int:artist_id>')
def artist_page(artist_id):
    sort_method = request.args.get('sort', 'rating')
    artist = Artist.query.get_or_404(artist_id)
    
    query = db.session.query(Album).filter(Album.artist_id == artist_id).outerjoin(Review).group_by(Album.id)
    
    if sort_method == 'rating':
        query = query.order_by(func.avg(Review.rating).desc())
    elif sort_method == 'newest':
        query = query.order_by(Album.year.desc())
    else:
        query = query.order_by(Album.year.asc())
        
    albums = query.all()
    return render_template('artist.html', artist=artist, albums=albums)


@main_bp.route('/album/<int:album_id>', methods=['GET', 'POST'])
def album_page(album_id):
    album = Album.query.get_or_404(album_id)
    if request.method == 'POST':
        new_review = Review(
            text=request.form.get('text'),
            rating=int(request.form.get('rating')),
            album_id=album.id
        )
        db.session.add(new_review)
        db.session.commit()
        return redirect(url_for('main.album_page', album_id=album.id))
    
    return render_template('album.html', album=album)