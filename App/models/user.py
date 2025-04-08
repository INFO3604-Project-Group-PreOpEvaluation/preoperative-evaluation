from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db

class User(db.Model, UserMixin):
    __abstract__ = True
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(1200), nullable=False)
    email = db.Column(db.String(150), nullable = False, unique = True)
    phone_number = db.Column(db.String(20), nullable = False, unique = True)
 
    def __init__(self, firstname, lastname, password, email, phone_number):
        self.firstname = firstname
        self.lastname = lastname
        self.set_password(password)
        self.email = email
        self.phone_number = phone_number

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    

    
