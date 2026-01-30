from flask import Blueprint, request, redirect, url_for
from flask_login import login_required
from models.models import db, Album

media_bp = Blueprint('media', __name__)

@media_bp.route('/seed')
@login_required
def seed_data():
    if not Album.query.first():
        data = [
            Album(title="The Dark Side of the Moon", artist="Pink Floyd", genre="Rock", year=1973, rating=5),
            Album(title="Thriller", artist="Michael Jackson", genre="Pop", year=1982, rating=5),
            Album(title="Random Access Memories", artist="Daft Punk", genre="Electronic", year=2013, rating=4),
            Album(title="Хуйня", artist="Daft Punk", genre="Electronic", year=2013, rating=1)
        ]
        db.session.add_all(data)
        db.session.commit()
    return redirect(url_for('main.index'))