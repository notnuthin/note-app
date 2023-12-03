from flask import render_template, redirect, flash, request, Blueprint, jsonify, url_for
from .forms import LoginForm, CreateAccountForm, CreateFolderForm, VerificationForm, ResetPassword, SendEmailCode
from app import app_obj, db, mail, serializer, BadSignature
from .models import User, Note, Folder
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/index.html")
@login_required
def index():
    notes = current_user.notes.all()
    return render_template('index.html', notes = notes)

@login_required
@app_obj.route("/homepage", methods = ['GET', 'POST'])
def homepage():
    # Queries the current user's notes and folders to be displayed on the homepage
    folders = current_user.folders.all()
    notes = current_user.notes.all()
    return render_template("homepage.html", folders = folders, notes = notes)


@app_obj.route('/new_folder', methods=['POST'])
def process_data():
    # get data from function, which should be the inputted folder name
    data = request.get_json()
    user_input = data.get('data')
    is_password_protected = data.get('is_password_protected', False)
    pin_code = data.get('pin_code')
    print("User input:", user_input)
    # make a folder with that information and save it
    f = Folder(name = user_input, user_id = current_user.id)
    if is_password_protected:
        f.is_password_protected = True
        f.pin_code = generate_password_hash(pin_code)
    db.session.add(f)
    db.session.commit()
    print("user added folder named ")
    print({user_input})
    return jsonify({'message': 'Data received successfully!'})

@app_obj.route('/new_note', methods=['POST'])
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
@app_obj.route('/updateDatabase', methods=['POST'])
def update_database():
    try:
        # gets data from the post request
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
@app_obj.route('/updateNote', methods = ['POST'])
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
@app_obj.route("/get_notes/<int:folder_id>")
def get_notes(folder_id):
    folder = Folder.query.filter_by(id=folder_id).first()
    # Returns the notes as an array of dictionaries for displaying
    if folder:
        if folder.is_password_protected:
            # Prompt the user for PIN code
            pin_code = request.args.get('pin_code')
            # Verify the PIN code
            if not pin_code:
                print("Incorrect PIN code")
                return jsonify({'error': 'PIN code is required for password-protected folder'}), 403
            hashed_pin_code = generate_password_hash(pin_code)
            print(f"Received PIN code: {pin_code}")
            if folder.pin_code is None or not check_password_hash(folder.pin_code, pin_code):
                print("Incorrect PIN code")
                return jsonify({'error': 'Incorrect PIN code'}), 403
        notes = [{'id': note.id, 'name': note.name} for note in folder.notes]
        return jsonify(notes)
    else:
        return jsonify({'error': 'Folder not found'}), 404

# Route to open a note
@login_required
@app_obj.route('/note/<int:note_id>')
def note_page(note_id):
    # Fetch note based on the note_id
    note = Note.query.filter_by(id=note_id).first()
    # Render the note page template with note info
    return render_template('note_page.html', note=note)


@app_obj.route('/delete_notes', methods=['POST'])
def delete_notes():
    try:
        data = request.json
        note_ids = data.get('note_ids', [])

        # Assuming Note is your SQLAlchemy model
        for note_id in note_ids:
            note = Note.query.get(note_id)
            if note:
                db.session.delete(note)

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
      
def generate_verify_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) #Generates a random verification code

@app_obj.route("/send_code", methods = ['GET', 'POST'])
def send_verify_code():
    form = SendEmailCode()
    if form.validate_on_submit():
        found_user = User.query.filter_by(email=form.email.data).first() #Verifies user if email is found
        if found_user:
            token = serializer.dumps({'user_id': found_user.id})
            reset_url = url_for('reset_password', user_id=found_user.id, token=token, _external=True)

            subject = 'Verification Code'
            body = f'Click the following link to reset your password: {reset_url}'
            recipient = form.email.data
            message = Message(subject=subject, recipients=[recipient], body=body)
            mail.send(message)
            #...
            return redirect('/verify')
    return render_template("send_code.html", form=form)

@app_obj.route("/verify", methods = ['GET', 'POST'])
def verify():
    return render_template("verify.html")

@app_obj.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_password(token):
    #TODO: Code password reset
    try:
        data = serializer.loads(token, max_age=3600)  # Adjust max_age as needed
        user_id = data.get('user_id')
        found_user = User.query.get(user_id)
    except BadSignature:
        flash('Invalid or expired reset token.')
        return redirect('/')

    form = ResetPassword()
    if form.validate_on_submit():
        if found_user:
            found_user.set_password(form.password.data)
            db.session.commit()
            flash('Password reset successfully. You can now log in with your new password.')
            return redirect('/login')
        else:
            flash('User not found.')
            return redirect('/')
    return render_template("reset_password.html", form=form)
    #...
