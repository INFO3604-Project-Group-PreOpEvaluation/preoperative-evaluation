import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.models import Questionnaire, Patient
from App.database import db
from App.controllers import (
    create_patient,
    create_questionnaire,
    get_questionnaire,
    get_all_questionnaires,
    get_all_questionnaires_json,
    get_questionnaire_by_patient_id,
    get_questionnaire_by_status,
    get_questionnaire_by_status_json,
    get_latest_questionnaire,
    set_patient_autofill_enabled
)

from datetime import datetime
import json


@pytest.fixture(autouse=True, scope="module")
def empty_db():
    """
    Fixture for creating an empty SQLite database before each test.
    """
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class AnesthiologistIntegrationTests(unittest.TestCase):
    """
    Integration tests for the Questionnaire controller functions.
    """

    def test_create_questionnaire(test_app):
        """
        Test creating a questionnaire with a valid patient ID and responses.
        """
        with test_app.app_context():
            # Ensure a patient is created before testing questionnaire creation
            sample_patient = create_patient(
                "John", "Doe", "password", "johndoe@mail.com", "1234567890"
            )
            assert sample_patient is not None  # Assert patient creation success

            # Call the function being tested
            responses = {"Q1": "Yes", "Q2": "No"}
            questionnaire = create_questionnaire(sample_patient.id, responses)

            # Assert that the questionnaire was successfully created
            assert questionnaire is not None
            assert questionnaire.patient_id == sample_patient.id
            assert questionnaire.status == "pending"
            assert questionnaire.responses == responses


    def test_get_questionnaire(setup_database):
        """
        Test retrieving a questionnaire by its ID.
        """
        patient = create_patient("John", "Doe", "password", "johndoe@mail.com", "1234567890")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})

        retrieved = get_questionnaire(questionnaire.id)
        assert retrieved is not None
        assert retrieved.id == questionnaire.id

    def test_get_all_questionnaires(setup_database):
        """
        Test retrieving all questionnaires.
        """
        patient = create_patient("John", "Doe", "password", "johndoe@mail.com", "1234567890")
        questionnaire1 = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})
        questionnaire2 = create_questionnaire(patient_id=patient.id, responses={"Q1": "No"})

        questionnaires = get_all_questionnaires()
        assert len(questionnaires) == 2

    def test_get_all_questionnaires_json(setup_database):
        """
        Test retrieving all questionnaires in JSON format.
        """
        questionnaire = Questionnaire(patient_id="123", responses={"Q1": "Yes"})
        db.session.add(questionnaire)
        db.session.commit()

        questionnaires_json = get_all_questionnaires_json()
        assert len(questionnaires_json) == 1
        assert questionnaires_json[0]["patient_id"] == "123"

    def set_patient_autofill_enabled(patient_id, enabled):
        """
        Set the autofill enabled status for a patient.
        """
        patient = get_patient_by_id(patient_id)
        if not patient:
            print(f"Error: Patient with ID {patient_id} not found.")
            return False
        patient.autofill_enabled = enabled
        db.session.commit()
        return True

    def test_get_questionnaire_by_patient_id(setup_database):
        """
        Test retrieving a questionnaire by patient ID.
        """
        questionnaire = Questionnaire(patient_id="123", responses={"Q1": "Yes"})
        db.session.add(questionnaire)
        db.session.commit()

        retrieved = get_questionnaire_by_patient_id("123")
        assert retrieved is not None
        assert retrieved.patient_id == "123"

    def test_get_questionnaire_by_status(setup_database):
        """
        Test retrieving questionnaires by status.
        """
        questionnaire = Questionnaire(patient_id="123", responses={"Q1": "Yes"}, status="completed")
        db.session.add(questionnaire)
        db.session.commit()

        completed_questionnaires = get_questionnaire_by_status("completed")
        assert len(completed_questionnaires) == 1
        assert completed_questionnaires[0].status == "completed"

    def test_get_questionnaire_by_status_json(setup_database):
        """
        Test retrieving questionnaires by status in JSON format.
        """
        questionnaire = Questionnaire(patient_id="123", responses={"Q1": "Yes"}, status="completed")
        db.session.add(questionnaire)
        db.session.commit()

        completed_json = get_questionnaire_by_status_json("completed")
        assert len(completed_json) == 1
        assert completed_json[0]["status"] == "completed"

    def test_get_latest_questionnaire(test_app):
        """
        Test retrieving the latest questionnaire for a patient.
        """
        with test_app.app_context():
            # Create sample questionnaires with valid `submitted_date` values
            questionnaire1 = Questionnaire(
                patient_id="123",
                responses={"Q1": "Yes"},
                submitted_date=datetime(2025, 1, 1)  # Valid datetime object
            )
            questionnaire2 = Questionnaire(
                patient_id="123",
                responses={"Q2": "No"},
                submitted_date=datetime(2025, 2, 1)
            )
            db.session.add(questionnaire1)
            db.session.add(questionnaire2)
            db.session.commit()

            # Retrieve the latest questionnaire
            latest = get_latest_questionnaire("123")
            assert latest is not None
            assert latest.responses == {"Q2": "No"}

