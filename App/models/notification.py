from datetime import datetime
from App.database import db
from .user import User
class Notification(db.Model):
    """
    Represents a notification sent to a user.
    """
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    # the user who received the notification
    # recipient_type = db.Column(db.String(50))  # 'anesthesiologist' or 'patient'
    # recipient_id = db.Column(db.Integer)
    anesthesiologist_id = db.Column(db.Integer, db.ForeignKey('anesthesiologist.id'), nullable=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=True)
    #  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # the title of the notification
    title = db.Column(db.String(220))
    # the message of the notification
    message = db.Column(db.String(220))
    # the time the notification was created
    timestamp=db.Column(db.DateTime,default = datetime.now())
    # whether the user has seen the notification
    seen = db.Column(db.Boolean, default=False)
    # patient = db.relationship('Patient', foreign_keys=[recipient_id])
    # anesthesiologist = db.relationship('Anesthesiologist', foreign_keys=[recipient_id])
    def __init__(self, recipientId, recipient_type, message, title):
        """
        Initializes a notification.
        
        :param recipientId: the id of the user who will receive the notification
        :param message: the message of the notification
        :param title: the title of the notification
        """
        self.recipientId = recipientId
        self.recipient_type = recipient_type
        self.message = message
        self.title = title
        self.timestamp = datetime.now()

    def get_json(self):
        """
        Returns a json representation of the notification.
        
        :return: a json representation of the notification
        """
        return{
            'id':self.id,
            'patient_id': self.recipientId,
            'recipient_type': self.recipient_type,
            'message': self.message,
            'title': self.title,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'seen': self.seen
        }
