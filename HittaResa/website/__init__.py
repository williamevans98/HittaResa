# Import av funktioner som vi använder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import wikipedia
from cachetools import cached


# Detta ska ändras
db = SQLAlchemy()
DB_NAME = "login_manager"

# Scriptet som fixar databasen


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'admin'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://sql11405569:8M3yX3fj8V@sql11.freemysqlhosting.net/sql11405569'
    db.init_app(app)

    # Importerar allt från template, static o.s.v.
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    # Definierar loginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.jinja_env.globals.update(fetch_from_wikipedia=fetch_from_wikipedia)

    return app


# Hämta från wikipedia
# Cache:ad för att få ner laddningstiden efter första gången
# TTL (time to live) är by default satt till 10800s (3hrs), sen hämtas summaryn igen från wikipedia
@cached(cache={})
def fetch_from_wikipedia(title):
    wikipedia.set_lang("sv")
    summary = wikipedia.summary(title, sentences=2)
    return summary

# Om databasen inte existerar så skapas den

def create_database(app):
    if not path.exists('website/' + DB_NAME):

        '''"CREATE TABLE login_manager (id int AUTO_INCREMENT PRIMARY KEY, email varchar(50), password varchar(50), first_name varchar(50));"'''

        db.create_all(app=app)
        print('Created Database!')
