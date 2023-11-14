from flask import render_template
from .forms import LoginForm, CreateAccountForm, VerificationForm
from app import app_obj, db
from flask import render_template
from flask import redirect
from flask import flash
from .models import User
import random
import string

@app_obj.route("/")
@app_obj.route("/index.html")
def index():
    name = 'Carlos'
    books = [ {'author': 'authorname1',
                'book':'bookname1'},
             {'author': 'authorname2',
              'book': 'bookname2'}]
    return render_template('hello.html',name=name, books=books)


@app_obj.route("/login", methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("validated")
        flash(f'Here are the input {form.username.data} and {form.password.data}')
        found_user = User.query.filter_by(username=form.username.data).first()
        print(found_user)
        return redirect("/")
    return render_template('login.html', form=form)

@app_obj.route("/create_account", methods = ['GET', 'POST'])
def signup():
    form = CreateAccountForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
            print('do something')
            print(f'this is the username of the user {form.username.data}')
            print(f'this is the password of the user {form.password.data}')
            u = User(username=form.username.data, password=form.password.data,
                     email=form.email.data)
            db.session.add(u)
            db.session.commit()
            return redirect('/')
    return render_template("create_account.html", form = form)

def generate_verify_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) #Generates a random verification code
def send_verify_code():
    return
@app_obj.route("/verify", methods = ['GET', 'POST'])
def verify():
    form = VerificationForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template("password_reset.html", form=form)