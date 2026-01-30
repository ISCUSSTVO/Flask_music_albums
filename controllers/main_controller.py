from flask import Blueprint, render_template, request, redirect, url_for
from models.models import Artist, Album, Review, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    artists = Artist.query.all()
    recent_albums = Album.query.order_by(Album.id.desc()).all()
    return render_template('index.html', artists=artists, albums=recent_albums)

@main_bp.route('/artist/<int:artist_id>')
def artist_page(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    return render_template('artist.html', artist=artist)

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