import pytest, logging, unittest
from datetime import datetime
from App.main import create_app
from App.database import db
from sqlalchemy.exc import IntegrityError
from App.controllers import (
    create_patient,
    create_medical_history,
    get_all_patients,
    get_patient_by_id,

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
    return create_patient("John", "Doe", "password", "johndoe@mail.com", "1234567890")

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
        patient = create_patient("Alice", "Smith",  "password", "alicesmith@mail.com", "9876543210")
        # Check that the patient was created successfully
        assert patient is not None
        # Verify the username of the created patient
        assert patient.email == "alicesmith@mail.com"
        assert patient.phone_number == "9876543210"
        assert patient.firstname == "Alice"
        assert patient.lastname == "Smith"

def test_create_duplicate_patient(test_app, sample_patient):
    '''
        Test that attempting to create an Anesthesiologist with a duplicate
        email or username results in the expected behavior
    '''
    with test_app.app_context():
        
        # Check that the duplicate patient was not created
        with pytest.raises(IntegrityError) as context:  # Or another appropriate exception
            duplicate_patient = create_patient("John", "Doe", "password", "johndoe@mail.com", "1234567890")
            assert("Integrity error while creating patient", str(context.exception))
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
        sample_patient = create_patient("John", "Doe", "password", "johndoe@mail.com", "1234567890")
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

def test_edit_medical_history(test_app, sample_patient):
    """
    Test the creation of medical history for a patient.

    Args:
        test_app: The Flask test application instance.
        sample_patient: The sample patient created by the test fixture.

    Asserts:
        The patient's medical history is successfully updated.
    """
    with test_app.app_context():
        # Define test inputs
        patient_id = sample_patient.id
        dateOfBirth = "1985-06-15"
        blood_type = "A+"
        weight = '68'
        height = '170'
        allergies = "Dust"
        medical_conditions = "Asthma"
        medication = "Ventolin"

        # Call the create_medical_history function
        updated_patient = create_medical_history(
            patient_id, dateOfBirth, blood_type, weight, height,
            allergies, medical_conditions, medication
        )

        # Assert the patient's medical history is updated correctly
        assert updated_patient is not None
        assert updated_patient.dateOfBirth == datetime.strptime(dateOfBirth, '%Y-%m-%d').date()
        assert updated_patient.blood_type == blood_type
        assert updated_patient.weight == weight
        assert updated_patient.height == height
        assert updated_patient.allergies == allergies
        assert updated_patient.medical_conditions == medical_conditions
        assert updated_patient.medication == medication

        assert updated_patient.med_history_updated is True

