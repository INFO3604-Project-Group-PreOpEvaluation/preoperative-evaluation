from App.database import db
from .user import User
from .notification import Notification
from .anesthesiologist import Anesthesiologist
from sqlalchemy.orm import aliased

class Patient(User):
    """
    A model for a patient user
    """

    __tablename__ = 'patient'
    type = db.Column(db.String(120), nullable=False, default='patient')
    dateOfBirth = db.Column(db.Date, nullable=True)
    sex = db.Column(db.String(2), nullable=True)
    blood_type = db.Column(db.String(8), nullable=True)
    weight = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    allergies = db.Column(db.String(250), nullable=True)
    medical_conditions = db.Column(db.String(250), nullable=True)
    medication = db.Column(db.String(250), nullable=True)
    med_history_updated = db.Column(db.Boolean, nullable=False, default=False)
    autofill_enabled = db.Column(db.Boolean, nullable=False, default=False)
    questionnaires = db.relationship('Questionnaire', backref='patient', lazy=True, cascade="all, delete-orphan")
    # notifications = db.Column(db.Integer, db.ForeignKey('notification.patient_id'), nullable=True)
    notifications = db.relationship('Notification', backref='patient', lazy=True, cascade="all, delete-orphan")
    # notifications = db.relationship('Notification', backref='patient', lazy=True, cascade="all, delete-orphan")


    def __init__(self, firstname, lastname, password, email, phone_number):
        """
          Initializes a Patient object

          Parameters
          ----------
          firstname : str
              The first name of the patient
          lastname : str
              The last name of the patient
          password : str
              The password of the patient
          email : str
              The email of the patient
          phone_number : str
              The phone number of the patient
        """
        # Validation logic for the fields
        self.validate_fields(firstname, lastname, password, email, phone_number)
        super().__init__(firstname, lastname, password, email, phone_number)
        self.type = 'patient'
    
    def validate_fields(self, firstname, lastname, password, email, phone_number):
        """
        Validates the input fields for creating a Patient object.
        """
        if not firstname or not lastname or not password or not email or not phone_number:
            raise ValueError("All fields for a patient are required.")
        if not isinstance(firstname, str) or not isinstance(lastname, str):
            raise TypeError("First name and last name must be strings.")
        if not isinstance(password, str):
            raise TypeError("Invalid field types for new patient.")
        if '@' not in email:
            raise ValueError("Email must contain '@'.")
        if not isinstance(phone_number, str) or not phone_number.isdigit():
            raise TypeError("Phone number must contain only digits.")

    
    def get_json(self):
        """
        Returns a JSON representation of the Patient object
        """
        return{
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone_number': self.phone_number,
            'sex': self.sex,
            'date_of_birth': self.dateOfBirth,
            'blood_type': self.blood_type,
            'weight': self.weight,
            'height': self.height,
            'allergies': self.allergies,
            'medical_conditions': self.medical_conditions,
            'medication': self.medication,
            'type': self.type

        }
