import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.models import Questionnaire, Patient
from App.database import db, create_db
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
    db.session.close()
    db.drop_all()


class QuestionnaireIntegrationTests(unittest.TestCase):
    """
    Integration tests for the Questionnaire controller functions.
    """

    def test_create_questionnaire(self):
        """
        Test creating a questionnaire with a valid patient ID and responses.
        """
        # Ensure a patient is created before testing questionnaire creation
        sample_patient = create_patient(
            "John", "Doe", "password", "johndoe99@mail.com", "1234567890"
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


    def test_get_questionnaire(self):
        """
        Test retrieving a questionnaire by its ID.
        """
        patient = create_patient("John", "Doe", "password", "johndoe7@mail.com", "1283567890")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})

        retrieved = get_questionnaire(questionnaire.id)
        assert retrieved is not None
        assert retrieved.id == questionnaire.id

    def test_get_all_questionnaires(setup_database):
        """
        Test retrieving all questionnaires.
        """
        patient = create_patient("John", "Doe", "password", "johndoe2@mail.com", "12397977790")
        questionnaire1 = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})
        questionnaire2 = create_questionnaire(patient_id=patient.id, responses={"Q1": "No"})

        questionnaires = get_all_questionnaires()
        assert len(questionnaires) == 3


    def test_get_questionnaire_by_patient_id(setup_database):
        """
        Test retrieving a questionnaire by patient ID.
        """
        patient = create_patient("John", "Doe", "password", "john2doe@mail.com", "129861190")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})

        retrieved = get_questionnaire_by_patient_id(patient.id) 
        assert retrieved is not None
        assert retrieved.patient_id == patient.id

    def test_get_questionnaire_by_status(self):
        """
        Test retrieving questionnaires by status.
        """
        patient = create_patient("John", "Doe", "password", "johnzdoe@mail.com", "880111890")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})
        questionnaire.status = "completed"

        completed_questionnaires = get_questionnaire_by_status("completed")
        assert len(completed_questionnaires) == 1
        assert completed_questionnaires[0].status == "completed"

    def test_get_latest_questionnaire(self):
        """
        Test retrieving the latest questionnaire for a patient.
        """
        patient = create_patient("John", "Doe", "password", "johnndoe99@mail.com", "8834561890")
        # Create sample questionnaires with valid `submitted_date` values
        questionnaire1 = create_questionnaire(
            patient_id=patient.id,
            responses={"Q1": "Yes"}
        )
        questionnaire1.submitted_date=datetime(2025, 1, 1)  # Valid datetime object
        questionnaire2 = create_questionnaire(
            patient_id=patient.id,
            responses={"Q2": "No"}
        )
        questionnaire2.submitted_date=datetime(2025, 2, 1)

        # Retrieve the latest questionnaire
        latest = get_latest_questionnaire(patient.id)
        assert latest is not None
        assert latest.responses == {"Q2": "No"}

