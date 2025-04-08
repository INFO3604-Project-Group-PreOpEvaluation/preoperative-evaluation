from App.database import db
from .patient import Patient
from datetime import datetime
import uuid

def generate_short_uuid():
    """
    Generates a short random UUID to be used as the primary key for questionnaires.
    """
    return str(uuid.uuid4())[:8]

class Questionnaire(db.Model):
    """
    Represents a questionnaire submitted by a patient to an anesthesiologist.
    """
    __tablename__ = 'questionnaire'
    id = db.Column(db.String(20), primary_key=True, default=generate_short_uuid, server_default='gen_random_uuid()')
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False) # Foreign key to Patient, db.ForeignKey('patient.id'))
    responses = db.Column(db.JSON, nullable=True) # Storing responses as JSON, if applicable
    operation_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    patient_notes = db.Column(db.String(1200), nullable=True)
    anesthesiologist_notes = db.Column(db.String(600), nullable=True)
    doctor_notes = db.Column(db.String(600), nullable=True)
    submitted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 


    # Initialization of Questionnaire with JSON fields
    def __init__(self, **kwargs):
        """
        Initialize a Questionnaire object with the given parameters.
        """
        super().__init__(**kwargs)
        # self.questions = kwargs.get('questions', [])
        self.patient_id = kwargs.get('patient_id', None)       
        self.responses = kwargs.get('responses', {})

           

    

