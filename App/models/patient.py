from App.database import db
from .user import User
from .crypto_utils import encrypt_value, decrypt_value

key = Fernet.generate_key()
cipher = Fernet(key)

class Patient(User):
    __tablename__ = 'patient'
    type = db.Column(db.String(120), nullable=False, default='patient')
    age = db.Column(db.Integer, nullable=True)
    _blood_type = db.Column('blood_type', db.LargeBinary, nullable=True)
    _weight = db.Column('weight', db.LargeBinary, nullable=True)
    _height = db.Column('height', db.LargeBinary, nullable=True)
    _allergies = db.Column('allergies', db.LargeBinary, nullable=True)
    _medical_conditions = db.Column('medical_conditions', db.LargeBinary, nullable=True)
    _medication = db.Column('medication', db.LargeBinary, nullable=True)
    @property
    def blood_type(self):
        return decrypt_value(self._blood_type)
    @blood_type.setter
    def blood_type(self, value):
        self._blood_type = encrypt_value(value)

    @property
    def height(self):
        return decrypt_value(self._height)
    @height.setter
    def height(self, value):
        self._height = encrypt_value(value)

    @property
    def weight(self):
        return decrypt_value(self._weight)
    @weight.setter
    def weight(self, value):
        self._weight = encrypt_value(value)

    @property
    def allergies(self):
        return decrypt_value(self._allergies)
    @allergies.setter
    def allergies(self, value):
        self._allergies = encrypt_value(value)

    @property
    def medical_conditions(self):
        return decrypt_value(self._medical_conditions)
    @medical_conditions.setter
    def medical_conditions(self, value):
        self._medical_conditions = encrypt_value(value)

    @property
    def medication(self):
        return decrypt_value(self._medication)
    @medication.setter
    def medication(self, value):
        self._medication = encrypt_value(value)

    med_history_updated = db.Column(db.Boolean, nullable=False, default=False)
    autofill_enabled = db.Column(db.Boolean, nullable=False, default=False)
    questionnaires = db.relationship('Questionnaire', backref='patient', lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship('Notification', backref='patient', lazy=True, cascade="all, delete-orphan")


    def __init__(self, firstname, lastname, username, password, email, phone_number):
        super().__init__(firstname, lastname, username, password, email, phone_number)
        self.type = 'patient'

    
    def get_json(self):
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
