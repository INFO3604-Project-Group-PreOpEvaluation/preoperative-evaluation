from datetime import datetime
from App.database import db
import uuid

class Notification(db.Model):
    """
    Represents a notification sent to a user.
    """
    __tablename__ = 'notification'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # the user who received the notification
    anesthesiologist_id = db.Column(db.String(36), db.ForeignKey('anesthesiologist.id'), nullable=True)
    patient_id = db.Column(db.String(36), db.ForeignKey('patient.id'), nullable=True)
    doctor_id = db.Column(db.String(36), db.ForeignKey('doctor.id'), nullable=True)
    # the title of the notification
    title = db.Column(db.String(220), nullable=False)
    # the message of the notification
    message = db.Column(db.String(220), nullable=False)
    # the time the notification was created
    timestamp=db.Column(db.DateTime,default = datetime.now())
    # whether the user has seen the notification
    seen = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, anesthesiologist_id, patient_id, doctor_id, message, title):
        """
        Initializes a notification.
        
        :param anesthesiologist_id: the id of the anesthesiologist who will receive the notification
        :param patient_id: the id of the patient who will receive the notification
        :param doctor_id: the id of the doctor who will receive the notification
        :param message: the message of the notification
        :param title: the title of the notification
        """
        self.id = str(uuid.uuid4())  # Generate a new UUID for each notification
        self.validate_fields(anesthesiologist_id, patient_id, doctor_id, message, title)
        self.anesthesiologist_id = anesthesiologist_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.message = message
        self.title = title
        self.timestamp = datetime.now()

    def validate_fields(self, anesthesiologist_id, patient_id, doctor_id, message, title):
        """
        Validates the input fields for creating a Notification object.
        """
        if (anesthesiologist_id is None and patient_id is None and doctor_id is None) or message is None or title is None:
            raise ValueError("All fields for notification are required")
        if not isinstance(message, str) or not isinstance(title, str):
            raise ValueError("Invalid field for notification: Message and title has to be string")
        if patient_id is not None and not isinstance(patient_id, str):
            raise ValueError("Invalid field for notification: Patient id has to be a string")
        if anesthesiologist_id is not None and not isinstance(anesthesiologist_id, str):
            raise ValueError("Invalid field for notification: Anesthesiologist id has to be a string")
        
    def get_json(self):
        """
        Returns a json representation of the notification.
        
        :return: a json representation of the notification
        """
        return{
            'id':self.id,
            'patient_id': self.patient_id,
            'anesthesiologist_id': self.anesthesiologist_id,
            'doctor_id': self.doctor_id,
            'message': self.message,
            'title': self.title,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'seen': self.seen
        }
