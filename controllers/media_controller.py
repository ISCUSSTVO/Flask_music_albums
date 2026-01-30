import os
from flask import Blueprint, redirect, url_for, render_template, request, current_app
from flask_login import login_required
from models.models import db, Album, Artist

media_bp = Blueprint('media', __name__)

@media_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_content():
    if request.method == 'POST':
        content_type = request.form.get('content_type')
        
        if content_type == 'artist':
            name = request.form.get('name')
            file = request.files.get('artist_image')
            
            if name and file:
               
                new_artist = Artist(name=name)
                db.session.add(new_artist)
                db.session.flush() 

                ext = os.path.splitext(file.filename)[1]
                filename = f"artist_{new_artist.id}{ext}"

                upload_path = os.path.join(current_app.root_path, 'static', 'img', 'artists', filename)
                file.save(upload_path)

                new_artist.image_url = filename
                db.session.commit()
        
        elif content_type == 'album':
            title = request.form.get('title')
            artist_id = request.form.get('artist_id')
            year = request.form.get('year')
            genre = request.form.get('genre')
            file = request.files.get('album_image')

            if title and artist_id and file:

                new_album = Album(title=title, artist_id=artist_id, year=year, genre=genre)
                db.session.add(new_album)
                db.session.flush() 

                ext = os.path.splitext(file.filename)[1]
                filename = f"album_{new_album.id}{ext}"

                upload_path = os.path.join(current_app.root_path, 'static', 'img', 'covers', filename)
                file.save(upload_path)

                new_album.cover_url = filename 
                db.session.commit()
                    
                return redirect(url_for('main.index'))

    artists = Artist.query.all()
    return render_template('add_content.html', artists=artists)

@media_bp.route('/delete-artist/<int:artist_id>', methods=['POST'])
@login_required
def delete_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)

    if artist.image_url:
        path = os.path.join(current_app.root_path, 'static', 'img', 'artists', artist.image_url)
        if os.path.exists(path):
            os.remove(path)
            
    db.session.delete(artist)
    db.session.commit()
    return redirect(url_for('main.index'))

@media_bp.route('/delete-album/<int:album_id>', methods=['POST'])
@login_required
def delete_album(album_id):
    album = Album.query.get_or_404(album_id)
    db.session.delete(album)
    db.session.commit()
    return redirect(url_for('main.index'))