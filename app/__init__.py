from flask import Flask

app_obj = Flask(__name__)

app_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess'
)

from app import routes