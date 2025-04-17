import pytest
import unittest
from datetime import datetime
from App.main import create_app
from App.database import db, create_db
from App.models import Notification
from sqlalchemy.exc import IntegrityError

from App.controllers import (
    create_patient,
    create_notification,
    create_doctor,
    create_anesthesiologist,
    get_user_notifications
)

'''
    Integration Tests
'''

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class NotificationIntegrationTests(unittest.TestCase):

    def test_notification_patient(self):
        """
        A Notification is created and sent to a patient.
        """

        # Create a new Patient instance
        newPatient = create_patient("Jane", "Doe", "password123", "jane.doe@example.com", "123497890")

        # Create a new Notification instance
        notification = create_notification(message="Test1", patient_id=newPatient.id, doctor_id=None, anesthesiologist_id=None, title="Notification1")
        # Save the Notification to the database
        db.session.add(notification)
        db.session.commit()

        # Verify that the patient has received the notification
        notifications = Notification.query.filter_by(patient_id=newPatient.id).all()
        assert len(notifications) == 1
        assert notifications[0].message == "Test1"
        assert notifications[0].title == "Notification1"
        assert notifications[0].patient_id == newPatient.id
        assert notifications[0].doctor_id is None
        assert notifications[0].anesthesiologist_id is None
    
    def test_notification_doctor(self):
        """
        A Notification is created and sent to a doctor.
        """

        # Create a new Doctor instance
        newDoctor = create_doctor("Jane", "Pierce", "password123", "jane.smith2@example.com", "0975554321")

        # Create a new Notification instance
        notification = create_notification(message="Test2", patient_id=None, doctor_id=newDoctor.id, anesthesiologist_id=None, title="Notification2")
 

        # Verify that the doctor has received the notification
        notifications = Notification.query.filter_by(doctor_id=newDoctor.id).all()
        assert len(notifications) == 1
        assert notifications[0].message == "Test2"
        assert notifications[0].title == "Notification2"
        assert notifications[0].doctor_id == newDoctor.id
        assert notifications[0].patient_id is None
        assert notifications[0].anesthesiologist_id is None

    def test_notification_anesthesiologist(self):
        """
        A Notification is created and sent to an anesthesiologist.
        """

        # Create a new Anesthesiologist instance
        newAnesthesiologist = create_anesthesiologist("Alice", "Johnson", "password123", "alice.johnson@example.com", "1122334455")

        # Create a new Notification instance
        notification = create_notification(message="Test3", patient_id=None, doctor_id=None, anesthesiologist_id=newAnesthesiologist.id, title="Notification3")

        # Verify that the anesthesiologist has received the notification
        notifications = Notification.query.filter_by(anesthesiologist_id=newAnesthesiologist.id).all()
        assert len(notifications) == 1
        assert notifications[0].message == "Test3"
        assert notifications[0].title == "Notification3"
        assert notifications[0].anesthesiologist_id == newAnesthesiologist.id
        assert notifications[0].patient_id is None
        assert notifications[0].doctor_id is None

    
    def test_get_user_notifications(self):
        """
        Get all notifications for a user Eg is a doctor
        """
        # Create a new Doctor instance
        newDoctor = create_doctor("Jane", "Smith", "password123", "jane.smith@example.com", "0987654321")
        patient = create_patient("John", "Doe", "password123", "john.doe@example.com", "1234567890")
        # Create a new Notification instance
        notification1 = create_notification(message="Test4", patient_id=None, doctor_id=newDoctor.id, anesthesiologist_id=None, title="Notification4")
        notification2 = create_notification(message="Test5", patient_id=None, doctor_id=newDoctor.id, anesthesiologist_id=None, title="Notification5")
        notification3 = create_notification(message="Test6", patient_id=patient.id, doctor_id=None, anesthesiologist_id=None, title="Notification6")

        # Save the Notifications to the database
        db.session.add_all([notification1, notification2, notification3])
        db.session.commit()

        # Verify that the doctor has received the notifications
        notifications = get_user_notifications('doctor', newDoctor.id)
        assert len(notifications) == 2

        assert notifications[0]['message'] == "Test5"
        assert notifications[0]['title'] == "Notification5"
        assert notifications[0]['doctor_id'] == newDoctor.id
        assert notifications[0]['patient_id'] is None
        assert notifications[0]['anesthesiologist_id'] is None

        assert notifications[1]['message'] == "Test4"
        assert notifications[1]['title'] == "Notification4"
        assert notifications[1]['doctor_id'] == newDoctor.id
        assert notifications[1]['patient_id'] is None
        assert notifications[1]['anesthesiologist_id'] is None

