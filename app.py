import os
import re
import transliterate
from flask import Flask
from flask_login import LoginManager
from models.models import db, User
from controllers.main_controller import main_bp
from controllers.media_controller import media_bp
from controllers.auth_controller import auth_bp


app = Flask(__name__)

app.config['SECRET_KEY'] = 'super-secret-key-change-me' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'instance', 'sqlite.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login' 
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(main_bp)
app.register_blueprint(media_bp)
app.register_blueprint(auth_bp)



@app.template_filter('slugify')
def slugify_filter(s):
    if not s:
        return ""
    try:
        s = transliterate.translit(s, 'ru', reversed=True)
    except:
        pass 
    
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '_', s)
    return s

with app.app_context():
    if not os.path.exists(os.path.join(app.root_path, 'instance')):
        os.makedirs(os.path.join(app.root_path, 'instance'))
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin') 
        db.session.add(admin)
        db.session.commit()
        print("Admin created: user='admin', pass='admin'")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)