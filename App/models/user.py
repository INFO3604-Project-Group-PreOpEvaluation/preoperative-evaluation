from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
import uuid

class User(db.Model, UserMixin):
    """
    User model for the database.
    
    This is the base class for all user types: patient, doctor and anesthesiologist.
    """
    __abstract__ = True
    __tablename__ = 'user'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(310), nullable=False)
    email = db.Column(db.String(150), nullable = False, unique = True)
    phone_number = db.Column(db.String(20), nullable = False, unique = True)

    def __init__(self, firstname, lastname, password, email, phone_number):
        """
        Constructor for User
        
        :param firstname: first name of the user
        :param lastname: last name of the user
        :param password: password of the user
        :param email: email of the user
        :param phone_number: phone number of the user
        """
        self.id = str(uuid.uuid4())  # Generate a new UUID for each user
        self.firstname = firstname
        self.lastname = lastname
        self.set_password(password)
        self.email = email
        self.phone_number = phone_number

    def get_json(self):
        """
        Returns a json representation of the user
        
        :return: a json representation of the user
        """
        return{
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone_number': self.phone_number
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    

    
