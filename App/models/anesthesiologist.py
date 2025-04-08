from App.database import db
from .user import User
from .questionnaire import Questionnaire

class Anesthesiologist(User):
    """
    Represents an anesthesiologist user in the database.

    In addition to the standard User fields, an anesthesiologist has a
    type field set to 'anesthesiologist'.
    """
    __tablename__ = 'anesthesiologist'
    type = db.Column(db.String(120), nullable=False, default='anesthesiologist')

    def __init__(self, firstname, lastname, password, email, phone_number):
        """
        Constructor for Anesthesiologist.

        """
        super().__init__(firstname, lastname, password, email, phone_number)
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
    

    