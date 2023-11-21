from flask import render_template
from .forms import LoginForm, CreateAccountForm, VerificationForm, SendEmail
from app import app_obj, db, mail
from flask import render_template
from flask import redirect
from flask import flash
from flask_mail import Message
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
                     email=form.email.data, vercode=None) #Added vercode
            db.session.add(u)
            db.session.commit()
            return redirect('/')
    return render_template("create_account.html", form = form)

def generate_verify_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) #Generates a random verification code

@app_obj.route("/send_code", methods = ['GET', 'POST'])
def send_verify_code():
    form = SendEmail()
    if form.validate_on_submit():
        found_user = User.query.filter_by(email=form.email.data).first() #Verifies user if email is found
        if found_user:
            code = generate_verify_code()
            found_user.vercode = code
            db.session.commit()
            #TODO: Code to send mail
            subject = 'Verification Code'
            body = f'Your verification code is: {code}'
            recipient = form.email.data
            message = Message(subject=subject, recipients=[recipient], body=body)
            mail.send(message)
            #...
            return redirect('/verify')
    return render_template("send_code.html", form=form)

@app_obj.route("/verify", methods = ['GET', 'POST'])
def verify():
    form = VerificationForm()
    if form.validate_on_submit():
        #TODO: Write code to verify user's code stored in database
        found_user = User.query.filter_by(vercode=form.code.data).first() #Finds user with the code
        if found_user:
            return redirect('/')
        else:
            redirect('/send_code')
        #...
    return render_template("verify.html", form=form)

@app_obj.route("/reset_password", methods = ['POST'])
def reset_password():
    #TODO: Code password reset
    return