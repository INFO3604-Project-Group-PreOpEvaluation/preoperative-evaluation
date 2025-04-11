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
        try: 
            if firstname is None or lastname is None or password is None or email is None or phone_number is None:
                raise ValueError
            super().__init__(firstname, lastname, password, email, phone_number)
        except ValueError:
            raise ValueError("All fields for a doctor are required.")
        except Exception as e:
            print(e, " - Error creating doctor")
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



