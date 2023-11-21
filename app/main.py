from flask import render_template, redirect, flash, request, Blueprint
from .forms import LoginForm, CreateAccountForm
from app import app_obj, db
from .models import User 
from flask_login import current_user, login_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index.html")
@login_required
def index():
    notes = current_user.notes.all()
    return render_template('index.html', notes = notes)


# @main.route("/login", methods = ['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#          return redirect('/')
#     form = LoginForm()
#     if form.validate_on_submit():
#         print("validated")
#         flash(f'Here are the input {form.username.data} and {form.password.data}')
#         found_user = User.query.filter_by(username=form.username.data).first()
#         if found_user is None or not found_user.check_password(form.paswword.data):
#              flash("Invalid username or password")
#              return redirect('/login')
#         login_user(found_user, remember = form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#              next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', form=form)

# @main.route("/logout")
# def logout():
#      logout_user()
#      return redirect('/')

# @main.route("/create_account", methods = ['GET', 'POST'])
# def signup():
#     form = CreateAccountForm()
#     print(form.validate_on_submit())
#     if form.validate_on_submit():
#             print('do something')
#             print(f'this is the username of the user {form.username.data}')
#             print(f'this is the password of the user {form.password.data}')
#             u = User(username=form.username.data, password=form.password.data,
#                      email=form.email.data)
#             db.session.add(u)
#             db.session.commit()
#             return redirect('/')
#     return render_template("create_account.html", form = form)