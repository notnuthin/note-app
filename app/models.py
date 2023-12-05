from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    notes = db.relationship('Note', backref = 'author', lazy = 'dynamic')
    folders = db.relationship('Folder', backref = 'author', lazy = 'dynamic')
    
    def set_password(self, password):
        self.password = generate_password_hash(password) #Password is saved as hash?

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<user {self.id}: {self.username}>'

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String, default = "Unnamed note on" + datetime.utcnow().strftime("%m/%d/%Y"))
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    folder = db.relationship('Folder', back_populates='notes')

class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String, nullable=False)
    notes = db.relationship('Note', back_populates='folder')
    is_password_protected = db.Column(db.Boolean, default=False) 
    pin_code = db.Column(db.String, nullable=True) #Will have pincode if password protected

    def check_code(self, pin_code):
        return check_password_hash(self.pin_code, pin_code)
    

    
    

    
