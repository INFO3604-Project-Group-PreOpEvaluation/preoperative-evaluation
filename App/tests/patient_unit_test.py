import os, tempfile, pytest, logging, unittest
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
        