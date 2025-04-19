import pytest
import unittest
from App.models import Questionnaire
from App.models.questionnaire import generate_short_uuid


'''
    Unit Tests
'''

class QuestionnaireUnitTests(unittest.TestCase):
    """
    Unit tests for the Questionnaire model and its respective controller functions.
    """
    def test_create_questionnaire(self):
        """
        A Questionnaire object is created and contains all fields from the input.
        """
        questionnaire = Questionnaire(patient_id=1, responses={"Q1": "a", "Q2": "b"})
        self.assertIsNotNone(questionnaire)
        self.assertEqual(questionnaire.patient_id, 1)
        self.assertEqual(questionnaire.responses, {"Q1": "a", "Q2": "b"})

    def test_update_questionnaire(self):
        """
        A Questionnaire object is created and then updated with new values.
        """
        questionnaire = Questionnaire(patient_id=1, responses={"Q1": "a", "Q2": "b"})
        
        # Update fields
        questionnaire.status = "accepted"
        questionnaire.patient_notes = "No notes"
        questionnaire.anesthesiologist_notes = "Healthy"
        questionnaire.doctor_notes = "Good patient"
        
        self.assertEqual(questionnaire.patient_id, 1)
        self.assertEqual(questionnaire.responses, {"Q1": "a", "Q2": "b"})
        self.assertEqual(questionnaire.status, "accepted")
        self.assertEqual(questionnaire.patient_notes, "No notes")
        self.assertEqual(questionnaire.anesthesiologist_notes, "Healthy")
        self.assertEqual(questionnaire.doctor_notes, "Good patient")

    def test_id_generation(self):
        """
        Verify that UUID of length 8 is generated for the questionnaire ID.
        """
        generated_id = generate_short_uuid()
        self.assertTrue(len(generated_id) == 8)
        self.assertTrue(isinstance(generated_id, str))


    def test_operation_date_nullable(self):
        """
        Verify that operation_date can be null.
        """
        questionnaire = Questionnaire(patient_id=1, responses={"Q1": "a", "Q2": "b"})
        self.assertIsNone(questionnaire.operation_date)
        
    def test_patient_notes_nullable(self):
        """
        Verify that patient_notes can be null.
        """
        questionnaire = Questionnaire(patient_id=1, responses={"Q1": "a", "Q2": "b"})
        self.assertIsNone(questionnaire.patient_notes)
        
    def test_anesthesiologist_notes_nullable(self):
        """
        Verify that anesthesiologist_notes can be null.
        """
        questionnaire = Questionnaire(patient_id=1, responses={"Q1": "a", "Q2": "b"})
        self.assertIsNone(questionnaire.anesthesiologist_notes)
        
    def test_doctor_notes_nullable(self):
        """
        Verify that doctor_notes can be null.
        """
        questionnaire = Questionnaire(patient_id=1, responses={"Q1": "a", "Q2": "b"})
        self.assertIsNone(questionnaire.doctor_notes)

    def test_questionnaire_to_json(self):
        """
        A Questionnaire object is created and its to_json method is called.
        """
        questionnaire = Questionnaire(
            patient_id=1, 
            responses={"Q1": "a", "Q2": "b"},
            status="pending",
            operation_date=None,
            patient_notes="Test notes",
            doctor_notes="Doctor observation"
        )
        questionnaire_json = questionnaire.get_json()

        # Test that the returned dictionary values match the Questionnaire object's attributes
        self.assertEqual(questionnaire_json['patient_id'], questionnaire.patient_id)
        self.assertEqual(questionnaire_json['responses'], questionnaire.responses)
        self.assertEqual(questionnaire_json['status'], questionnaire.status)
        self.assertEqual(questionnaire_json['patient_notes'], questionnaire.patient_notes)
        self.assertEqual(questionnaire_json['doctor_notes'], questionnaire.doctor_notes)

    def test_invalid_questionnaire_field(self):
        """
        Verify that creating a Questionnaire with invalid fields raises errors.
        """
        with self.assertRaises(ValueError) as context:
            questionnaire = Questionnaire(patient_id=None, responses={"Q1": "a", "Q2": "b"})
            # Assuming patient_id is required
            self.assertTrue("Invalid field for questionnaire" in str(context))

