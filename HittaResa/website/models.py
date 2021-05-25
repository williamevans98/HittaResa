from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Definerar databasen uppbyggnad.
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
