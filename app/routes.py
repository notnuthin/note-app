from flask import render_template
from .forms import LoginForm
from app import app_obj

@app_obj.route("/")
@app_obj.route("/index.html")
def index():
    name = 'Carlos'
    books = [ {'author': 'authorname1',
                'book':'bookname1'},
             {'author': 'authorname2',
              'book': 'bookname2'}]
    return render_template('hello.html',name=name, books=books)

@app_obj.route("/hello")
def hello():
    return "Hello World!"

@app_obj.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
