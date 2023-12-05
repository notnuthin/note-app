from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Optional, Length
import email_validator

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CreateAccountForm(FlaskForm):
    name = StringField('Full name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Create Account')

class CreateFolderForm(FlaskForm):
    name = StringField('Untitled', validators=[DataRequired()])
    is_password_protected = BooleanField('Password Protect Folder')
    pin_code = StringField('PIN Code', validators=[Optional(), Length(4, 4, "PIN code must be 4 characters")])
    submit = SubmitField('Make Folder')

class VerificationForm(FlaskForm):
    code = StringField('Verification', validators=[DataRequired()])
    submit = SubmitField('Verify')

class SendEmailCode(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Send Email')

class ResetPassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Change Password')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name')
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Save Changes')

class DeleteProfileForm(FlaskForm):
    confirmation = StringField('Enter', validators=[DataRequired()])
    submit = SubmitField('Delete Profile')