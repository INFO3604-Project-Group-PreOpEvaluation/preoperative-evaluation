from App.database import db
from .user import User
from .notification import Notification
from .anesthesiologist import Anesthesiologist
from sqlalchemy.orm import aliased
class Patient(User):
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
    # notifications = db.relationship('Notification', foreign_keys='Notification.recipient_id', primaryjoin=lambda: db.and_(Notification.recipient_type == 'patient', Notification.recipient_id == Patient.id))
    # notifications = db.relationship('Notification', foreign_keys='Notification.recipient_id', primaryjoin=lambda: db.and_(Notification.recipient_type == 'patient', Notification.recipient_id == Patient.id), remote_side=[aliased(Anesthesiologist).id])
    # notifications = db.relationship('Notification', foreign_keys='Notification.recipient_id', primaryjoin='Notification.recipient_id == Patient.id and Notification.recipient_type == "patient"',cascade="all, delete-orphan")
    def __init__(self, firstname, lastname, password, email, phone_number):
        super().__init__(firstname, lastname, password, email, phone_number)
        self.type = 'patient'

    
    def get_json(self):
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
