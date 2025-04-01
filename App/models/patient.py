from cryptography.fernet import Fernet
from App.database import db
from .user import User

key = Fernet.generate_key()
cipher = Fernet(key)

class Patient(User):
    __tablename__ = 'patient'
    type = db.Column(db.String(120), nullable=False, default='patient')
    age = db.Column(db.Integer, nullable=True)
    blood_type = db.Column(db.LargeBinary, nullable=True)
    weight = db.Column(db.LargeBinary, nullable=True)
    height = db.Column(db.LargeBinary, nullable=True)
    allergies = db.Column(db.LargeBinary, nullable=True)
    medical_conditions = db.Column(db.LargeBinary, nullable=True)
    medication = db.Column(db.LargeBinary, nullable=True)
    @property
    def blood_type(self):
        return cipher.decrypt(self.blood_type).decode if self.blood_type else None
    @blood_type.setter
    def blood_type(self, value):
        self.blood_type = cipher.encrypt(value.encode()) if value else None

    @property
    def height(self):
        return cipher.decrypt(self.height).decode if self.height else None
    @height.setter
    def height(self, value):
        self.height = cipher.encrypt(value.encode()) if value else None

    @property
    def weight(self):
        return cipher.decrypt(self.weight).decode if self.weight else None
    @weight.setter
    def weight(self, value):
        self.weight = cipher.encrypt(value.encode()) if value else None

    @property
    def allergies(self):
        return cipher.decrypt(self.allergies).decode if self.allergies else None
    @allergies.setter
    def allergies(self, value):
        self.allergies = cipher.encrypt(value.encode()) if value else None
    
    @property
    def medical_conditions(self):
        return cipher.decrypt(self.medical_conditions).decode if self.medical_conditions else None
    @medical_conditions.setter
    def medical_conditions(self, value):
        self.medical_conditions = cipher.encrypt(value.encode()) if value else None
    
    @property
    def medication(self):
        return cipher.decrypt(self.medication).decode if self.medication else None
    @medication.setter
    def medication(self, value):
        self.medication = cipher.encrypt(value.encode()) if value else None

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
