# Import av funktioner som vi använder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import wikipedia
from db_connection import *


# Detta ska ändras
db = SQLAlchemy()
DB_NAME = "login_manager"

# Scriptet som fixar databasen


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'admin'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://' + database_name + ':' + database_password + '@' + database_host + '/' + database_user
    db.init_app(app)

    # Importerar allt från template, static o.s.v.
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    from .fetch_from_wikipedia import summaries

    # Definierar loginManager
    user = LoginManager()
    user.login_view = 'auth.login'
    user.init_app(app)

    @user.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.jinja_env.globals.update(summaries=summaries)

    return app

    app.close()