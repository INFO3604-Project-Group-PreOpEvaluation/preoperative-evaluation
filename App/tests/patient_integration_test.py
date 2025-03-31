import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_patient,
    create_medical_history,
    get_all_patients,
    get_patient_by_id,
    set_patient_autofill_enabled
)

LOGGER = logging.getLogger(__name__)

'''
Integration Test
'''
@pytest.fixture
def test_app():
    """
    Creates a test version of the Flask app for each test run

    Yields:
        app: The test app instance
    """
    app = create_app("testing")
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
def client(test_app):
    """
    Creates a test client for the test app

    Returns:
        client: The test client
    """
    return test_app.test_client()

@pytest.fixture
def sample_patient():
    """
    Creates a sample patient object with the specified details.

    Returns:
        patient: The sample patient object.
    """
    return create_patient("John", "Doe", "johndoe", "password", "johndoe@mail.com", "1234567890")

class UsersIntegrationTests(unittest.TestCase):
    def test_create_patient(test_app):
        """
        Test the creation of a patient.

        Args:
            test_app: The Flask test application instance.

        Asserts:
            The patient is successfully created and the username is correct.
        """
        with test_app.app_context():
            # Attempt to create a new patient
            patient = create_patient("Alice", "Smith", "alicesmith", "password", "alicesmith@mail.com", "9876543210")
            # Check that the patient was created successfully
            assert patient is not None
            # Verify the username of the created patient
            assert patient.username == "alicesmith"

    def test_create_duplicate_patient(test_app, sample_patient):
        with test_app.app_context():
            # Attempt to create a duplicate patient
            duplicate_patient = create_patient("John", "Doe", "johndoe", "password", "johndoe@mail.com", "1234567890")
            # Check that the duplicate patient was not created
            assert duplicate_patient is None

    def test_get_all_patients(test_app):
        """
        Test the retrieval of all patients.

        Args:
            test_app: The Flask test application instance.

        Asserts:
            The list of patients is not empty and the first patient is the sample patient.
        """
        with test_app.app_context():
            # Create a sample patient
            sample_patient = create_patient("John", "Doe", "johndoe", "password", "johndoe@mail.com", "1234567890")
            # Retrieve all patients
            patients = get_all_patients()
            # Check that the list of patients is not empty
            assert len(patients) > 0
            # Verify the first patient in the list is the sample patient
            assert patients[0].id == sample_patient.id

    def test_get_patient_by_id(test_app, sample_patient):
        """
        Test the retrieval of a patient by ID.

        Args:
            test_app: The Flask test application instance.
            sample_patient: The sample patient created by the test fixture.

        Asserts:
            The retrieved patient is the same as the sample patient.
        """
        with test_app.app_context():
            # Retrieve a patient by ID
            retrieved_patient = get_patient_by_id(sample_patient.id)
            # Check that the retrieved patient is the same as the sample patient
            assert retrieved_patient.id == sample_patient.id
