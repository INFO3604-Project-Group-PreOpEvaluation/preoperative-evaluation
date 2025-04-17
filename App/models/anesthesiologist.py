from App.database import db
from .user import User
from .questionnaire import Questionnaire
from .notification import Notification

class Anesthesiologist(User):
    """
    Represents an anesthesiologist user in the database.

    In addition to the standard User fields, an anesthesiologist has a
    type field set to 'anesthesiologist'.
    """
    __tablename__ = 'anesthesiologist'
    type = db.Column(db.String(120), nullable=False, default='anesthesiologist')
    # notifications = db.Column(db.Integer, db.ForeignKey('notification.anesthesiologist_id'), nullable=True)
    notifications = db.relationship('Notification', backref='anesthesiologist', lazy=True, cascade="all, delete-orphan")
    def __init__(self, firstname, lastname, password, email, phone_number):
        """
        Constructor for Anesthesiologist.

        """
        try:
            if firstname is None or lastname is None or password is None or email is None or phone_number is None:
                raise ValueError
            super().__init__(firstname, lastname, password, email, phone_number)

        except ValueError:
            raise ValueError("All fields for an anesthesiologist are required.")
        except Exception as e:
            print(e, " - Error creating anesthesiologist")
            
        self.type = 'anesthesiologist'

    def get_json(self):
        """
        Return a JSON representation of the Anesthesiologist.

        :return: JSON representation of the Anesthesiologist
        """
        return{
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone_number': self.phone_number,
            'type': self.type
        }
    

    