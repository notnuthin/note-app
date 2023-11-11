from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app_obj = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app_obj)

with app_obj.app_context():
    from app.models import User
    db.create_all()

from app import routes