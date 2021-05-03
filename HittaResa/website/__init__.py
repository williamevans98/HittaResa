# Import av funktioner som vi använder
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import wikipedia


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
    from .fetch_from_wikipedia import summaries

    create_database(app)

    # Definierar loginManager
    user = LoginManager()
    user.login_view = 'auth.login'
    user.init_app(app)

    @user.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.jinja_env.globals.update(summaries=summaries)

    return app


# Om databasen inte existerar så skapas den


def create_database(app):
    if not path.exists('website/' + DB_NAME):

        '''"CREATE TABLE user (user_id int AUTO_INCREMENT PRIMARY KEY, email varchar(150), password varchar(150));"'''

        db.create_all(app=app)
        print('Created Database!')