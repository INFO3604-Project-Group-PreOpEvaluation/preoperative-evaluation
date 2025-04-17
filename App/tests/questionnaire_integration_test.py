import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.models import Questionnaire, Patient
from App.database import db
from App.controllers import (
    create_patient,
    get_patient_by_id,
    create_questionnaire,
    get_questionnaire,
    get_all_questionnaires,
    get_all_questionnaires_json,
    get_questionnaire_by_patient_id,
    get_questionnaire_by_status,
    get_questionnaire_by_status_json,
    get_latest_questionnaire,
    update_questionnaire
)

from datetime import datetime
import json

@pytest.fixture
def test_app():
    """
    Creates a test version of the Flask app for each test run

    Yields:
        app: The test app instance
    """
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    with app.app_context():
        # Create all tables and schemas in the database
        db.create_all()
        # Yield the app so that each test can use it
        yield app
        # Remove the database session after each test
        db.session.remove()
        # Drop all tables and schemas after each test
        db.drop_all()

@pytest.fixture
def setup_database():
    # Setup in-memory database
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()

def test_create_questionnaire(test_app):
    with test_app.app_context():
        # Ensure a patient is created before testing questionnaire creation
        sample_patient = create_patient(
            "John", "Doe", "johndoe", "password", "johndoe@mail.com", "1234567890"
        )
        assert sample_patient is not None  # Assert patient creation success

        # Call the function being tested
        responses = {"Q1": "Yes", "Q2": "No"}
        questionnaire = create_questionnaire("1234567890", responses)

        # Assert that the questionnaire was successfully created
        assert questionnaire is not None
        assert questionnaire.patient_id == "1234567890"
        assert questionnaire.responses == responses


def test_get_questionnaire(setup_database):
    questionnaire = Questionnaire(patient_id="12345", responses={"Q1": "Yes"})
    db.session.add(questionnaire)
    db.session.commit()

    retrieved = get_questionnaire(questionnaire.id)
    assert retrieved is not None
    assert retrieved.id == questionnaire.id

def test_get_all_questionnaires(setup_database):
    questionnaire1 = Questionnaire(patient_id="123", responses={"Q1": "Yes"})
    questionnaire2 = Questionnaire(patient_id="124", responses={"Q1": "No"})
    db.session.add(questionnaire1)
    db.session.add(questionnaire2)
    db.session.commit()

    questionnaires = get_all_questionnaires()
    assert len(questionnaires) == 2

def test_get_all_questionnaires_json(setup_database):
    questionnaire = Questionnaire(patient_id="123", responses={"Q1": "Yes"})
    db.session.add(questionnaire)
    db.session.commit()

    questionnaires_json = get_all_questionnaires_json()
    assert len(questionnaires_json) == 1
    assert questionnaires_json[0]["patient_id"] == "123"

def set_patient_autofill_enabled(patient_id, enabled):
    patient = get_patient_by_id(patient_id)
    if not patient:
        print(f"Error: Patient with ID {patient_id} not found.")
        return False
    patient.autofill_enabled = enabled
    db.session.commit()
    return True

def test_get_questionnaire_by_patient_id(setup_database):
    questionnaire = Questionnaire(patient_id="123", responses={"Q1": "Yes"})
    db.session.add(questionnaire)
    db.session.commit()

    retrieved = get_questionnaire_by_patient_id("123")
    assert retrieved is not None
    assert retrieved.patient_id == 123

def test_get_questionnaire_by_status(setup_database):
    questionnaire = Questionnaire(patient_id="123", responses={"Q1": "Yes"}, status="completed")
    db.session.add(questionnaire)
    db.session.commit()

    completed_questionnaires = get_questionnaire_by_status("completed")
    assert len(completed_questionnaires) == 1
    assert completed_questionnaires[0].status == "completed"

def test_get_questionnaire_by_status_json(setup_database):
    questionnaire = Questionnaire(patient_id="123", responses={"Q1": "Yes"}, status="completed")
    db.session.add(questionnaire)
    db.session.commit()

    completed_json = get_questionnaire_by_status_json("completed")
    assert len(completed_json) == 1
    assert completed_json[0]["status"] == "completed"

def test_get_latest_questionnaire(test_app):
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

def test_update_questionnaire(setup_database, sample_questionnaire):
    updated = update_questionnaire(sample_questionnaire.id, doctor_notes="Updated notes", operation_date="2025-05-20", status="Approved")
    
    assert updated is not None
    assert updated.doctor_notes == "Updated notes"
    assert updated.operation_date == "2025-05-20"
    assert updated.status == "Approved"