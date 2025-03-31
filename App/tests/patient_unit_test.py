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
            firstname="John", 
            lastname="Doe", 
            username="johndoe", 
            password="securepassword", 
            email="johndoe@example.com", 
            phone_number="1234567890"
        )
        # Assertions to validate the function
        self.assertIsNotNone(new_patient)
        self.assertEqual(new_patient.firstname, "John")
        self.assertEqual(new_patient.lastname, "Doe")
        self.assertEqual(new_patient.username, "johndoe")
        self.assertEqual(new_patient.email, "johndoe@example.com")
        self.assertEqual(new_patient.phone_number, "1234567890")

    def test_create_medical_history(self):
        new_patient = Patient(
            firstname="John", 
            lastname="Doe", 
            username="johndoe", 
            password="securepassword", 
            email="johndoe@example.com", 
            phone_number="1234567890"
        )

        update_patient = medical_history(
            patient_id=new_patient.id,
            age=30,
            blood_type="O+",
            weight=80,
            height=170,
            allergies="peanuts",
            medical_conditions="diabetes",
            medication="metformin"
        )

        # Assertions to validate the function
        self.assertIsNotNone(update_patient)
        self.assertEqual(update_patient.age, 30)
        self.assertEqual(update_patient.blood_type, "O+")
        self.assertEqual(update_patient.weight, 80)
        self.assertEqual(update_patient.height, 170)
        self.assertEqual(update_patient.allergies, "peanuts")
        self.assertEqual(update_patient.medical_conditions, "diabetes")
        self.assertEqual(update_patient.medication, "metformin")

    def test_get_all_patients(mock_query):
        # Mock return value
        mock_query.all.return_value = [
            Patient("John", "Doe", "johndoe", "pass123", "johndoe@example.com", "1234567890"),
        ]
        
        patients = get_all_patients()
        assert len(patients) == 1
        assert patients[0].username == "johndoe"
        

