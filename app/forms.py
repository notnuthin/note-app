from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
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

class VerificationForm(FlaskForm):
    code = StringField('Verification', validators=[DataRequired()])
    submit = SubmitField('Verify')

class SendEmail(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Send Email')