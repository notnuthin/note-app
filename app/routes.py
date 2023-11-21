from flask import render_template
from .forms import LoginForm, CreateAccountForm, CreateFolderForm
from app import app_obj, db
from flask import render_template
from flask import redirect
from flask import flash, request, jsonify
from .models import User, Note, Folder
import time

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
        return render_template("homepage.html", User=found_user)
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

@app_obj.route("/homepage", methods = ['GET', 'POST'])
def homepage():
    # users = User.query.all()
    folders = Folder.query.all()
    notes = Note.query.all()
    print("hello")
    # print(users)
    formF = CreateFolderForm()
    
    print(formF.validate_on_submit())
    if formF.validate_on_submit():
        # data = request.get_json()
        # print("User input:", data)
        f = Folder(name = formF.name.data, id = 0)
        db.session.add(f)
        db.session.commit()
        print({formF.name.data})
        return redirect("/homepage")
    return render_template("homepage.html", form = formF, folders = folders, notes = notes)#users = users)

@app_obj.route('/new_folder', methods=['POST'])
def process_data():
    # get data from function
    data = request.get_json()
    user_input = data.get('data')
    print("User input:", user_input)
    # make a folder and then save it
    f = Folder(name = user_input, user = 0)
    db.session.add(f)
    db.session.commit()
    print("user added")
    print({user_input})
    return jsonify({'message': 'Data received successfully!'})
    
@app_obj.route("/note")
def notepage():
    return render_template("note_page.html")

