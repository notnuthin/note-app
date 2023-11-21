from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
#checking if reset work
app_obj = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app_obj)

with app_obj.app_context():
    from app.models import User, Note, Folder
    #db.drop_all() #this command deletes the tables so you can add new ones
    db.create_all()
from app import routes