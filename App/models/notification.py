from datetime import datetime
from App.database import db

class Notification(db.Model):
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    recipientId = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(220))
    message = db.Column(db.String(220))
    timestamp=db.Column(db.DateTime,default = datetime.now())
    seen = db.Column(db.Boolean, default=False)
    
    def __init__(self, recipientId, message, title):
        self.recipientId = recipientId
        self.message = message
        self.title = title
        self.timestamp = datetime.now()

    def get_json(self):
        return{
            'id':self.id,
            'patient_id': self.recipientId,
            'message': self.message,
            'title': self.title,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'seen': self.seen
        }