from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_login import LoginManager

app_obj = Flask(__name__)

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


login_manager = LoginManager(app_obj)
login_manager.login_view = 'auth.login'

from .models import User
@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

from app import main, auth, models
