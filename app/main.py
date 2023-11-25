from flask import render_template, redirect, flash, request, Blueprint, jsonify
from .forms import LoginForm, CreateAccountForm, CreateFolderForm
from app import app_obj, db
from .models import User, Note, Folder
from flask_login import current_user, login_user, logout_user, login_required

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index.html")
@login_required
def index():
    notes = current_user.notes.all()
    return render_template('index.html', notes = notes)

@app_obj.route("/homepage", methods = ['GET', 'POST'])
def homepage():
    # users = User.query.all()
    folders = Folder.query.all()
    notes = Note.query.all()
    print("hello")
    # print(users)
    formF = CreateFolderForm()
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

@app_obj.route('/new_note', methods=['POST'])
def new_note():
    # get data from function
    data = request.get_json()
    user_input = data.get('data')
    if user_input=="":
        user_input = "untitled"
    print("User input:", user_input)
    # make a note and then save it
    n = Note(name = user_input, user_id = 0)
    db.session.add(n)
    db.session.commit()
    print("user added")
    print({user_input})
    return jsonify({'message': 'Data received successfully!'})

@app_obj.route('/updateDatabase', methods=['POST'])
def update_database():
    try:
        print("ran")
        data = request.json
        selected_folder_id = data.get('selectedFolder')
        selected_notes_ids = data.get('selectedNotes')
        print(selected_notes_ids)
         # Update the folder_id and folder attribute for each selected note
        for note_id in selected_notes_ids:
            note = Note.query.get(note_id)
            if note:
                # Update the note.folder and note.folder_id attributes
                note.folder_id = selected_folder_id
                print("Note folder_id updated")
                folder = Folder.query.get(selected_folder_id)
                note.folder = folder

                # Append the note to the notes relationship in the folder
                if folder and note not in folder.notes:
                    folder.notes.append(note)
        # Commit the changes
        db.session.commit()

        # Return a success response
        return jsonify({'success': True})

    except Exception as e:
        # Handle errors and return an error response
        return jsonify({'success': False, 'error': str(e)})
    
# Route to serve notes data for a given folder ID
@app_obj.route("/get_notes/<int:folder_id>")
def get_notes(folder_id):
    folder = Folder.query.filter_by(id=folder_id).first()
    if folder:
        notes = [{'id': note.id, 'name': note.name} for note in folder.notes]
        return jsonify(notes)
    else:
        return jsonify({'error': 'Folder not found'}), 404

@app_obj.route('/note/<int:note_id>')
def note_page(note_id):
    # Fetch note based on the note_id
    note = Note.query.filter_by(id=note_id).first()
    # Render the note page template 
    return render_template('note_page.html', note=note)



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