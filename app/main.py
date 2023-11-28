from flask import render_template, redirect, flash, request, Blueprint, jsonify, url_for
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

@login_required
@main.route("/homepage", methods = ['GET', 'POST'])
def homepage():
    # Queries the current user's notes and folders to be displayed on the homepage
    folders = current_user.folders.all()
    notes = current_user.notes.all()
    return render_template("homepage.html", folders = folders, notes = notes)


@main.route('/new_folder', methods=['POST'])
def process_data():
    # get data from function, which should be the inputted folder name
    data = request.get_json()
    user_input = data.get('data')
    print("User input:", user_input)
    # make a folder with that information and save it
    f = Folder(name = user_input, user_id = current_user.id)
    db.session.add(f)
    db.session.commit()
    print("user added folder named ")
    print({user_input})
    return jsonify({'message': 'Data received successfully!'})

@main.route('/new_note', methods=['POST'])
def new_note():
    # get data from function, which should be the inputted note name
    data = request.get_json()
    user_input = data.get('data')
    if user_input=="":
        user_input = "untitled"
    print("User input:", user_input)
    # make a note with the inputted name, or untitled if the field was left blank
    n = Note(name = user_input, user_id = current_user.id, body = "Start writing your note here!")
    db.session.add(n)
    db.session.commit()
    print("user added note named ")
    print({user_input})
    return jsonify({'message': 'Data received successfully!'})

#this route is for moving notes to a folder
@main.route('/updateDatabase', methods=['POST'])
def update_database():
    try:
        #gets data from the post request
        data = request.json
        selected_folder_id = data.get('selectedFolder')
        selected_notes_ids = data.get('selectedNotes')
        print(selected_folder_id)
         # Update the folder_id and folder attribute for each selected note
        for note_id in selected_notes_ids:
            note = Note.query.get(note_id)
            if note:
                # Update the note.folder and note.folder_id attributes
                note.folder_id = selected_folder_id
                print( note.name + " folder_id updated to " + selected_folder_id )
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
        # Return an error response
        return jsonify({'success': False, 'error': str(e)})
    
#Route to save the note data 
@main.route('/updateNote', methods = ['POST'])
def update_Note():
    try:
        # Data includes the note id and updated content
        data = request.json
        note_id = data.get('note_id')
        note_content = data.get('note_content')
        note = Note.query.get(note_id)
        
        # change the note content
        if note:
            note.body = note_content
        db.session.commit()

        # success and error responses
        return jsonify({'success':True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Route to send the notes for a given folder ID
@main.route("/get_notes/<int:folder_id>")
def get_notes(folder_id):
    folder = Folder.query.filter_by(id=folder_id).first()
    # Returns the notes as an array of dictionaries for displaying
    if folder:
        notes = [{'id': note.id, 'name': note.name} for note in folder.notes]
        return jsonify(notes)
    else:
        return jsonify({'error': 'Folder not found'}), 404

# Route to open a note
@login_required
@main.route('/note/<int:note_id>', methods = ['GET'])
def note_page(note_id):
    print(f"Accessing note page for note ID: {note_id}")
    # Fetch note based on the note_id
    note = Note.query.filter_by(id=note_id).first()
    # Render the note page template with note info
    print(note)
    return render_template('note_page.html', note=note)

@login_required
@main.route('/search', methods = ['GET'])
def search():
    search_expression = request.args.get('search_expression')
    print(search_expression)
    note = Note.query.filter_by(name = search_expression).first()
    #print(note.id)
    if note is None:
        return {"result": None}
    else:
        redirect_url = url_for('main.note_page', note_id=note.id)
        print(f"Redirect URL: {redirect_url}")  # Add this line for debugging
        return {"result": redirect_url}