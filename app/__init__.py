from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail 
from itsdangerous import URLSafeTimedSerializer, BadSignature
import shutil

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

serializer = URLSafeTimedSerializer(app_obj.config['SECRET_KEY'])
basedir = os.path.abspath(os.path.dirname(__file__))

app_obj.static_folder = 'static'

app_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app_obj)
migrate = Migrate(app_obj, db)

from .auth import auth as auth_blueprint
app_obj.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app_obj.register_blueprint(main_blueprint)

# with app_obj.app_context():
#      from app.models import User, Note, Folder
#      db.drop_all() #this command deletes the tables so you can add new ones
#      db.create_all()



login_manager = LoginManager(app_obj)
login_manager.login_view = 'auth.login'

from .models import User
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

from app import main, auth, models

