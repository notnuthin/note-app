from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)

    def set_password(self, password):
        self.password = generate_password_hash(password) #Password is saved as hash?

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<user {self.id}: {self.username}>'
    