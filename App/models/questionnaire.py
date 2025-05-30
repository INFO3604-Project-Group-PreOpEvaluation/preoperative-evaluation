from App.database import db
from datetime import datetime
import uuid

def generate_short_uuid():
    return str(uuid.uuid4())[:8]

def generate_uuid():
    return str(uuid.uuid4())


class Questionnaire(db.Model):
    """
    Represents a questionnaire submitted by a patient to an anesthesiologist.
    """
    __tablename__ = 'questionnaire'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=False)
    responses = db.Column(db.JSON, nullable=True) # Storing responses as JSON, if applicable
    operation_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    doctor_status = db.Column(db.String(20), nullable=False, default='pending')
    patient_notes = db.Column(db.String(1200), nullable=True)
    anesthesiologist_notes = db.Column(db.String(600), nullable=True)
    doctor_notes = db.Column(db.String(600), nullable=True)
    submitted_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    patient_notes = db.Column(db.String(1200), nullable=True)

    # Initialization of Questionnaire with JSON fields
    def __init__(self, **kwargs):
        """
        Initialize a Questionnaire object with the given parameters.
        """
        try:
            self.id = generate_uuid()  # Generate a new UUID for each questionnaire
            self.patient_id = kwargs['patient_id']
            if self.patient_id is None:
                raise ValueError()
            self.responses = kwargs.get('responses', {})
            self.submitted_date = datetime.now()
        except ValueError as e:
            raise ValueError(f"Invalid field for questionnaire: {e}")


    def get_json(self):
        """
        Converts the Questionnaire object into a JSON-serializable dictionary.

        Returns:
            dict: A dictionary representation of the Questionnaire.
        """
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "responses": self.responses,
            "operation_date": self.operation_date,
            "status": self.status,
            "doctor_status": self.doctor_status,
            "patient_notes": self.patient_notes,
            "anesthesiologist_notes": self.anesthesiologist_notes,
            "doctor_notes": self.doctor_notes,
            "submitted_date": self.submitted_date.isoformat() if self.submitted_date else None,
        }


