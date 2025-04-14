import pytest
import unittest
from datetime import datetime
from App.models import Notification


'''
    Unit Tests
'''

class NotificationUnitTests(unittest.TestCase):
    """
    Unit tests for the Notification model and its respective controller functions.
    """
    def test_new_notification(self):
        """
        A Notification object is created and contains all fields from the input.
        """
        notification = Notification(
            anesthesiologist_id=None, 
            patient_id=1, 
            message="Test1", 
            title="Notification1"
        )
        self.assertIsNotNone(notification)
        self.assertEqual(notification.message, "Test1")
        self.assertEqual(notification.title, "Notification1")
        self.assertEqual(notification.patient_id, 1)
        self.assertIsNone(notification.anesthesiologist_id)
        self.assertIsNotNone(notification.timestamp)
        self.assertFalse(notification.seen)

    def test_notification_for_patient(self):
        """
        A Notification for a patient is created with correct attributes.
        """
        notification = Notification(
            message="Test1", 
            patient_id=1, 
            anesthesiologist_id=None, 
            title="Notification1"
        )
        self.assertIsNotNone(notification)
        self.assertEqual(notification.patient_id, 1)
        self.assertIsNone(notification.anesthesiologist_id)
        self.assertEqual(notification.message, "Test1")
        self.assertEqual(notification.title, "Notification1")

    def test_notification_for_anesthesiologist(self):
        """
        A Notification for an anesthesiologist is created with correct attributes.
        """
        notification = Notification(
            message="Test1", 
            patient_id=None, 
            anesthesiologist_id=1, 
            title="Notification1"
        )
        self.assertIsNotNone(notification)
        self.assertIsNone(notification.patient_id)
        self.assertEqual(notification.anesthesiologist_id, 1)
        self.assertEqual(notification.message, "Test1")
        self.assertEqual(notification.title, "Notification1")

    def test_seen_notification(self):
        """
        A Notification's seen attribute can be set to True.
        """
        notification = Notification(
            message="Test1", 
            patient_id=1, 
            anesthesiologist_id=None, 
            title="Notification1"
        )
        notification.seen = True
        self.assertTrue(notification.seen)

    def test_notification_timestamp(self):
        """
        A Notification's timestamp is set to the current time upon creation.
        """
        before_creation = datetime.now()
        notification = Notification(
            message="Test1", 
            patient_id=1, 
            anesthesiologist_id=None, 
            title="Notification1"
        )
        after_creation = datetime.now()
        
        self.assertIsNotNone(notification.timestamp)
        self.assertIsInstance(notification.timestamp, datetime)
        
        # Checks that timestamp is between before and after creation
        self.assertTrue(before_creation <= notification.timestamp <= after_creation)

    def test_notification_to_json(self):
        """
        A Notification object is created and its to_json method is called.
        """
        notification = Notification(
            message="Test1", 
            patient_id=1, 
            anesthesiologist_id=None, 
            title="Notification1"
        )
        notification_json = notification.get_json()
        
        # Test that the returned dictionary values match the Notification object's attributes
        self.assertEqual(notification_json['patient_id'], notification.patient_id)
        self.assertEqual(notification_json['anesthesiologist_id'], notification.anesthesiologist_id)
        self.assertEqual(notification_json['message'], notification.message)
        self.assertEqual(notification_json['title'], notification.title)
        self.assertEqual(notification_json['timestamp'], notification.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(notification_json['seen'], notification.seen)

    def test_notification_invalid_fields(self):
        """
        Verify that creating a Notification with invalid fields raises errors.
        """
        with self.assertRaises(ValueError) as context:
            notification = Notification(
                message=123,
                patient_id="1", 
                anesthesiologist_id="4a", 
                title=99
            )
            self.assertTrue("Invalid field for notification" in str(context))

    def test_notification_missing_fields(self):
        """
        Verify that creating a Notification without required fields raises errors.
        """
        with self.assertRaises(ValueError) as context:
            notification = Notification(
                message=None, 
                patient_id=None, 
                anesthesiologist_id=None, 
                title="Notification1"
            )
            self.assertTrue("All fields for notification are required" in str(context))