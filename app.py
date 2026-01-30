import os
from flask import Flask
from models.models import db
from controllers.main_controller import main_bp
from controllers.media_controller import media_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-very-secret'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'instance', 'sqlite.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


app.register_blueprint(main_bp)
app.register_blueprint(media_bp)

with app.app_context():
    if not os.path.exists(os.path.join(app.root_path, 'instance')):
        os.makedirs(os.path.join(app.root_path, 'instance'))
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)