from App.database import db
from .user import User

class Doctor(User):
    """
    A doctor model which extends the user model.
    """
    __tablename__ = 'doctor'
    type = db.Column(db.String(120), nullable=False, default='doctor')

    def __init__(self, firstname, lastname, password, email, phone_number):
        """
        Initializes a doctor.
        
        """
        super().__init__(firstname, lastname, password, email, phone_number)
        self.type = 'doctor'

    def get_json(self):
        """
        Returns a json representation of the doctor.
        :return: A json representation of the doctor.
        """
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone_number': self.phone_number,
            'type': self.type
        }



