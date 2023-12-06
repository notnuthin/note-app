from flask import render_template, redirect, flash, make_response, request, Blueprint, jsonify, url_for, send_file
from .forms import LoginForm, CreateAccountForm, CreateFolderForm, VerificationForm, ResetPassword, SendEmailCode, ProfileForm, DeleteProfileForm
from app import app_obj, db, mail, serializer, BadSignature
from .models import User, Note, Folder
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash
from io import BytesIO
import random
import string
from docx import Document
#from flask_weasyprint import HTML, render_pdf

main = Blueprint('main', __name__)

# @main.route("/")
# @main.route("/index.html")
# @login_required
# def index():
#     notes = current_user.notes.all()
#     return render_template('index.html', notes = notes)


@main.route("/")
@main.route("/homepage", methods = ['GET', 'POST'])
@login_required
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
    results = []
    search_expression = request.args.get('search_expression')
    filter = request.args.get('folder')
    print(search_expression)
    print(filter)
    if filter == "All folders":
        notes = Note.query.filter_by(name = search_expression).all()
    else:
        notes = Note.query.filter_by(name=search_expression, id =filter).all()
    if notes is None:
        return {"result": None}
    else:
        for note in notes:
            results.append({'name': note.name, 'url': url_for('main.note_page', note_id=note.id)})
    return {"results": results}

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

# Route to export notes in various formats
@app_obj.route('/export/<output_format>', methods=['POST'])
def export_notes(output_format):
    try:
        data = request.json
        note_content = data.get('note_content')
        print(note_content)

        # Check if note content is empty
        if not note_content:
            raise RuntimeError("Empty note content")

        if output_format == 'pdf':
            # Use WeasyPrint for PDF conversion
            html_content = f"<pre>{note_content}</pre>"
            pdf = HTML(string=html_content).write_pdf()
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=temp_note.pdf'
        elif output_format == 'docx':
            # Use python-docx for docx conversion
            doc = Document()
            doc.add_paragraph(note_content)
            docx_output = BytesIO()
            doc.save(docx_output)
            docx_output.seek(0)
            response = send_file(docx_output, as_attachment=True, download_name='temp_note.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        else:
            # Send plain text back
            response = make_response(note_content)
            response.headers['Content-Type'] = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment; filename=temp_note.txt'

        return response

    except Exception as e:
        # Return an error response
        return jsonify({'success': False, 'error': str(e)}), 500

#TODO: Add Profile page route. Read requirement
# This method is used to call user_profile method, this initalizes user's id.
@login_required
@app_obj.route('/profile', methods=['GET', 'POST'])
def profile():
    print("Route working")
    print("User id is: ", current_user.id)
    return redirect(url_for('user_profile', user_id=current_user.id))

@login_required
@app_obj.route('/user_profile/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    print("Route working")
    form = ProfileForm()
    return render_template("profile.html", user_id=user_id, form=form)

#This method updates the user profile
@login_required
@app_obj.route('/update_profile', methods=['POST'])
def update_profile():
    form = ProfileForm(request.form)  # Instantiate the ProfileForm
    if form.validate():
        # Check the password and update the profile if valid
        if current_user.check_password(form.password.data):
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.name = form.name.data
            db.session.commit()
            flash('Profile updated successfully!')
            return redirect('/')
        else:
            flash('Incorrect password. Profile not updated.')
            logout_user()  # Log out the user on incorrect password
            return redirect('/login')
    return render_template('profile.html', form=form)

#TODO: Delete profile method
@login_required
@app_obj.route('/delete_profile', methods=['GET', 'POST'])
def delete_profile():
    form = DeleteProfileForm()
    if form.validate():
        if(form.confirmation.data == "DELETE"):
            # Delete the user's notes
            Note.query.filter_by(user_id=current_user.id).delete()
            # Delete the user's folders
            Folder.query.filter_by(user_id=current_user.id).delete()
            # Delete the user and log them out
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            flash('Profile deleted successfully.')
            return redirect('/signup')
        else:
            logout_user()
            flash('Incorrect Validation')
            return redirect('/login')
    return render_template('delete_profile.html', form=form)

