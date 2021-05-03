from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "userdatabase.db"

# Import av funktioner som vi använder

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'admin'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

# Konfigurerar SQLAlchemy

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    # Definierar loginManager
    user = LoginManager()
    user.login_view = 'auth.login'
    user.init_app(app)

    @user.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):

        '''"CREATE TABLE user (user_id int AUTO_INCREMENT PRIMARY KEY, email varchar(150), password varchar(150));"'''

        db.create_all(app=app)
        print('Created Database!')
