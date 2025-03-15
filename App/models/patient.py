from App.database import db
from .user import User

class Patient(User):
    """
    A model for a patient user
    """

    __tablename__ = 'patient'
    type = db.Column(db.String(120), nullable=False, default='patient')
    age = db.Column(db.Integer, nullable=True)
    blood_type = db.Column(db.String(8), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    allergies = db.Column(db.String(250), nullable=True)
    medical_conditions = db.Column(db.String(250), nullable=True)
    medication = db.Column(db.String(250), nullable=True)
    med_history_updated = db.Column(db.Boolean, nullable=False, default=False)
    autofill_enabled = db.Column(db.Boolean, nullable=False, default=False)
    questionnaires = db.relationship('Questionnaire', backref='patient', lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='patient', lazy=True, cascade="all, delete-orphan")


    def __init__(self, firstname, lastname, username, password, email, phone_number):
        """
        Initializes a Patient object

        Parameters
        ----------
        firstname : str
            The first name of the patient
        lastname : str
            The last name of the patient
        username : str
            The username of the patient
        password : str
            The password of the patient
        email : str
            The email of the patient
        phone_number : str
            The phone number of the patient
        """
        super().__init__(firstname, lastname, username, password, email, phone_number)
        self.type = 'patient'
    
    def get_json(self):
        """
        Returns a JSON representation of the Patient object
        """
        return{
            'id': self.id,
            'username': self.username,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone_number': self.phone_number,
            'age': self.age,
            'blood_type': self.blood_type,
            'weight': self.weight,
            'height': self.height,
            'allergies': self.allergies,
            'medical_conditions': self.medical_conditions,
            'medication': self.medication,
            'type': 'patient'

        }
