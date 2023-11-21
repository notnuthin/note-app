from flask import Blueprint, render_template, redirect, url_for, flash
from . import db
from .forms import LoginForm, CreateAccountForm
from .models import User
from flask_login import login_user, current_user, login_required, logout_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        print("validated")
        print(f'Here are the input {form.username.data} and {form.password.data}')
        found_user = User.query.filter_by(username=form.username.data).first()
        print(f"Found user:{found_user}")
        if found_user is None or not found_user.check_password(form.password.data):
             flash("Invalid username or password")
             return redirect(url_for('auth.login'))
        login_user(found_user, remember = form.remember_me.data)
        return redirect('/')
    return render_template('login.html', form=form, page_type = 'login')

@auth.route("/signup", methods = ['GET', 'POST'])
def signup():
    form = CreateAccountForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
            print('do something')
            print(f'this is the username of the user {form.username.data}')
            print(f'this is the password of the user {form.password.data}')
            user = User.query.filter_by(email = form.email.data).first()
            if user:
                flash('Email address already exists')
                return redirect(url_for('auth.signup'))
            u = User(username=form.username.data, email=form.email.data)
            u.set_password(form.password.data)
            db.session.add(u)
            db.session.commit()
            print("user added")
            return redirect('/')
    return render_template("signup.html", form = form, page_type = 'signup')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')