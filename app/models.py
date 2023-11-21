from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    vercode = db.Column(db.String, nullable=True) #Verification code column, can be null

    #TODO: Set Verification_code method, Verification_check method
    def set_verification(self, vercode):
        self.vercode = vercode
 
    def set_password(self, password):
        self.password = generate_password_hash(password) #Password is saved as hash?

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<user {self.id}: {self.username}>'
    