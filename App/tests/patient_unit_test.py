import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Patient
from App.controllers import (
    create_patient,
    create_medical_history,
    get_all_patients,
    get_patient_by_id,
    set_patient_autofill_enabled
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class PatientUnitTests(unittest.TestCase):

    def test_create_patient(self):
        new_patient = Patient(
            firstname="John1", 
            lastname="Doe1", 
            password="securepassword", 
            email="johndoe@example.com", 
            phone_number="1234567890"
        )
        # Assertions to validate the function
        self.assertIsNotNone(new_patient)
        self.assertEqual(new_patient.firstname, "John1")
        self.assertEqual(new_patient.lastname, "Doe1")
        self.assertEqual(new_patient.email, "johndoe@example.com")
        self.assertEqual(new_patient.phone_number, "1234567890")
        self.assertEqual(new_patient.password is not None, True)

    def test_patient_to_json(self):
        new_patient = Patient(
            firstname="John2", 
            lastname="Doe2", 
            password="password123", 
            email="johndoe@example.com", 
            phone_number="1234567890"
        )
        patient_json = new_patient.get_json()
        
        self.assertEqual(patient_json['firstname'], "John2")
        self.assertEqual(patient_json['lastname'], "Doe2")
        self.assertEqual(patient_json['email'], "johndoe@example.com")
        self.assertEqual(patient_json['phone_number'], "1234567890")

    def test_patient_missing_fields(self):
        with self.assertRaises(ValueError) as context:  
            new_patient = Patient(firstname=None, lastname=None,
                                  password=None, email=None, phone_number=None)
            self.assertEqual(str(context), "All fields for a patient are required.")

    def test_patient_password_security(self):
        new_patient = Patient(
            firstname="Secure", 
            lastname="User", 
            password="sTr0ngP@ssw0rd", 
            email="secure.user@example.com", 
            phone_number="0123456789"
        )

        assert len(new_patient.password) >= 8  # Example: Enforce length
        assert any(char.isupper() for char in new_patient.password)  # Example: Enforce uppercase
        assert any(char.islower() for char in new_patient.password)  # Example: Enforce lowercase
        assert any(char.isdigit() for char in new_patient.password)  # Example: Enforce digit
    
    def test_patient_to_json_special_characters(self):
        new_patient = Patient(
            firstname="Jöhn", 
            lastname="Döe", 
            password="p@ssword123", 
            email="john!doe@example.com", 
            phone_number="1234567890"
        )
        patient_json = new_patient.get_json()
        
        self.assertEqual(patient_json['firstname'], "Jöhn")
        self.assertEqual(patient_json['lastname'], "Döe")
        self.assertEqual(patient_json['email'], "john!doe@example.com")
        self.assertEqual(patient_json['phone_number'], "1234567890")

    def test_new_patient_invalid_field_types(self):
        """
        Test that creating a patient object with invalid field types raises an error
        """
        # Test firstname as an integer
        with self.assertRaises(TypeError) as context:
            Patient(firstname=123, lastname="Doe", password="password123", email="x123@example.com", phone_number="1234567890")
            self.assertEqual(str(context), "Invalid field types for new patient.")

        # Test lastname as an integer
        with self.assertRaises(TypeError) as context:
            Patient(firstname="John", lastname=345, password="password123", email="x123@example.com", phone_number="1234567890")
            self.assertEqual(str(context), "Invalid field types for new patient.")

        # Test password as an integer
        with self.assertRaises(TypeError) as context:
            Patient(firstname="John", lastname="Doe", password=123, email="x123@example.com", phone_number="1234567890")
            self.assertEqual(str(context), "Invalid field types for new patient.")

        # Test email as invalid
        with self.assertRaises(ValueError) as context:
            Patient(firstname="John", lastname="Doe", password="password123", email="x123", phone_number="1234567890")
            self.assertEqual(str(context), "Invalid field types for new patient2.")

        # Test phone_number as invalid
        with self.assertRaises(TypeError) as context:
            Patient(firstname="John", lastname="Doe", password="password123", email="x123@example.com", phone_number="phone#")
            self.assertEqual(str(context), "Invalid field types for new patient.")
