from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail 
import os
#checking if reset work
app_obj = Flask(__name__)

#Adding email 
app_obj.config['SECRET_KEY'] = "cool_and_safe_secret_key" #No clue why we need this, the tutorial says so
app_obj.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app_obj.config['MAIL_PORT'] = 465  #Use port 465 for secure SSL/TLS
app_obj.config['MAIL_USE_TLS'] = False
app_obj.config['MAIL_USE_SSL'] = True  #Use SSL for secure connection
app_obj.config['MAIL_USERNAME'] = 'easynotes131@gmail.com'
app_obj.config['MAIL_PASSWORD'] = 'ozpgzwxnteijbkmc'
app_obj.config['MAIL_DEFAULT_SENDER'] = 'your_email@example.com'

mail = Mail(app_obj) 
#...
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