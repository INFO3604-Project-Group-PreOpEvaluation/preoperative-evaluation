import os, tempfile, pytest, logging, unittest

from App.main import create_app
from App.models import Questionnaire, Patient
from App.database import db, create_db
from App.controllers import (
    create_patient,
    create_anesthesiologist,
    create_doctor,
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

from datetime import datetime, date
import json


@pytest.fixture(autouse=True, scope="function")
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

    def test_create_questionnaire(self, empty_db=empty_db):
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


    def test_get_questionnaire(self, empty_db=empty_db):
        """
        Test retrieving a questionnaire by its ID.
        """
        patient = create_patient("John", "Doe", "password", "johndoe7@mail.com", "1283567890")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})

        retrieved = get_questionnaire(questionnaire.id)
        assert retrieved is not None
        assert retrieved.id == questionnaire.id

    def test_get_all_questionnaires(self,empty_db=empty_db):
        """
        Test retrieving all questionnaires.
        """
        patient = create_patient("John", "Doe", "password", "johndoe2@mail.com", "12397977790")
        questionnaire1 = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})
        questionnaire2 = create_questionnaire(patient_id=patient.id, responses={"Q1": "No"})
        questionnaire3 = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})
        questionnaires = get_all_questionnaires()
        assert len(questionnaires) == 3


    def test_get_questionnaire_by_patient_id(self,empty_db=empty_db):
        """
        Test retrieving a questionnaire by patient ID.
        """
        patient = create_patient("John", "Doe", "password", "john2doe@mail.com", "129861190")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})

        retrieved = get_questionnaire_by_patient_id(patient.id) 
        assert retrieved is not None
        assert retrieved.patient_id == patient.id

    def test_get_questionnaire_by_status(self,empty_db=empty_db):
        """
        Test retrieving questionnaires by status.
        """
        patient = create_patient("John", "Doe", "password", "johnzdoe@mail.com", "880111890")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})
        questionnaire.status = "completed"

        completed_questionnaires = get_questionnaire_by_status("completed")
        assert len(completed_questionnaires) == 1
        assert completed_questionnaires[0].status == "completed"

    def test_get_latest_questionnaire(self,empty_db=empty_db):
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

    def test_add_user_response(self,empty_db=empty_db):
        """
        Test updating a questionnaire.
        """
        patient = create_patient("John", "Doe", "password", "johnndoe909@mail.com", "4534561890")
        anesthesiologist = create_anesthesiologist("John", "Doe", "password", "johnndoe909@mail.com", "4634561890")
        doctor = create_doctor("John", "Doe", "password", "johnndoe909@mail.com", "4834561890")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})
        
        # Test updating a questionnaire
        updated = update_questionnaire(questionnaire.id, user_type=anesthesiologist.type, anesthesiologist_notes="Anestiesthesiologist Notes")
        assert updated is not None
        updated2 = update_questionnaire(questionnaire.id, user_type=doctor.type, doctor_notes="Doctor Notes")
        assert updated2 is not None
        updated3 = update_questionnaire(questionnaire.id, user_type=patient.type, patient_notes="Notes")
        assert updated3 is not None
        assert updated3.responses == {"Q1": "Yes"}
        assert "Notes" in questionnaire.patient_notes
        updated = update_questionnaire(questionnaire.id, user_type=patient.type, patient_notes="Notes2")
        assert "Notes2" in questionnaire.patient_notes
        assert "Doctor Notes" in questionnaire.doctor_notes
        assert "Anestiesthesiologist Notes" in questionnaire.anesthesiologist_notes
    
    def test_approve_deny_questionnaire_anesthesiologist(self,empty_db=empty_db):
        """
        Test updating a questionnaire.
        """
        patient = create_patient("John", "Doe", "password", "johnndoe909@mail.com", "4534561890")
        anesthesiologist = create_anesthesiologist("John", "Doe", "password", "johnndoe909@mail.com", "4634561890")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})
        questionnaire2 = create_questionnaire(patient_id=patient.id, responses={"Q1": "No"})
        questionnaire.status = "completed"
        questionnaire2.status = "completed"

        # Test updating a questionnaire - Anestesiologist
        updated = update_questionnaire(questionnaire.id, user_type=anesthesiologist.type, status="declined")
        updated2 = update_questionnaire(questionnaire2.id, user_type=anesthesiologist.type, anesthesiologist_notes="Explain your reasons", status="declined_w_c")
        
        assert updated is not None
        assert updated2 is not None
        assert updated.status == "declined"
        assert updated2.status == "declined_w_c"
        assert "Explain your reasons" in updated2.anesthesiologist_notes

        # Test updating a questionnaire - Patients
        
        updated3 = update_questionnaire(questionnaire2.id, user_type=patient.type, patient_notes="My reasons were x")
    
        assert updated3 is not None
        assert updated3.status == "declined_w_c"

        updated4 = update_questionnaire(questionnaire2.id, user_type=anesthesiologist.type, anesthesiologist_notes="Valid reasoning", status="approved_w_c")

        # Tests if system prevents users from updating a declined questionnaire
        updated5 = update_questionnaire(questionnaire.id, user_type=anesthesiologist.type, anesthesiologist_notes="Valid reasoning", status="approved_w_c")
        assert updated4 is not None
        assert updated5 is not None
        assert updated4.status == "approved_w_c"
        assert "My reasons were x" in updated3.patient_notes
        assert updated5.status == "declined"
        assert updated5.anesthesiologist_notes == ''

        

    def test_approve_deny_questionnaire_doctor(self,empty_db=empty_db):
        """
        Test updating a questionnaire.
        """
        patient = create_patient("John", "Doe", "password", "johnndoe909@mail.com", "4534561890")
        anesthesiologist = create_anesthesiologist("John", "Doe", "password", "johnndoe909@mail.com", "4634561890")
        doctor = create_doctor("John", "Doe", "password", "johnndoe909@mail.com", "4834561890")
        questionnaire = create_questionnaire(patient_id=patient.id, responses={"Q1": "Yes"})
        questionnaire2 = create_questionnaire(patient_id=patient.id, responses={"Q1": "No"})
        questionnaire3 = create_questionnaire(patient_id=patient.id, responses={"Q1": "No"})
        questionnaire4 = create_questionnaire(patient_id=patient.id, responses={"Q1": "No"})

        questionnaire.status = "completed"
        questionnaire2.status = "completed"
        questionnaire3.status = "completed"
        questionnaire4.status = "completed"

        # Assertions for questionnaire
        assert questionnaire is not None
        assert questionnaire.status == "completed"
        assert questionnaire.patient_id == patient.id
        assert questionnaire.responses == {"Q1": "Yes"}

        # Assertions for questionnaire2
        assert questionnaire2 is not None
        assert questionnaire2.status == "completed"
        assert questionnaire2.patient_id == patient.id
        assert questionnaire2.responses == {"Q1": "No"}

        # Assertions for questionnaire3
        assert questionnaire3 is not None
        assert questionnaire3.status == "completed"
        assert questionnaire3.patient_id == patient.id
        assert questionnaire3.responses == {"Q1": "No"}

        # Assertions for questionnaire4
        assert questionnaire4 is not None
        assert questionnaire4.status == "completed"
        assert questionnaire4.patient_id == patient.id
        assert questionnaire4.responses == {"Q1": "No"}

        # Case 1 - Anesthesiologist approves, doctor approves
        updated_case1 = update_questionnaire(questionnaire.id, user_type=anesthesiologist.type, status="approved")
        updated2_case1 = update_questionnaire(questionnaire.id, user_type=doctor.type, doctor_status="approved", operation_date=datetime(2023, 1, 1))
        assert updated_case1 is not None
        assert updated2_case1 is not None
        assert updated_case1.status == "approved"
        assert updated2_case1.doctor_status == "approved"
        assert updated2_case1.operation_date == date(2023, 1, 1)

        # Case 2 - Anesthesiologist approves, doctor declines
        updated_case2 = update_questionnaire(questionnaire2.id, user_type=anesthesiologist.type, status="approved")
        updated2_case2 = update_questionnaire(questionnaire2.id, user_type=doctor.type, doctor_status="declined")
        assert updated_case2 is not None
        assert updated2_case2 is not None
        assert updated_case2.status == "approved"
        assert updated2_case2.doctor_status == "declined"

        # Case 3 - Anesthesiologist approves, doctor declines with clarification -> anesthesiologist
        updated_case3 = update_questionnaire(questionnaire3.id, user_type=anesthesiologist.type, status="approved")
        assert updated_case3 is not None
        assert updated_case3.status == "approved"

        updated2_case3 = update_questionnaire(questionnaire3.id, user_type=doctor.type, doctor_status="declined_w_c_a", doctor_notes="My reasons were x")
        assert updated2_case3 is not None
        assert updated2_case3.doctor_status == "declined_w_c_a"
        assert updated2_case3.doctor_notes == "My reasons were x"

        updated3_case3 = update_questionnaire(questionnaire3.id, user_type=anesthesiologist.type, status="approved", anesthesiologist_notes="My reasons were y")
        assert updated3_case3 is not None
        assert updated3_case3.status == "approved"
        assert updated3_case3.anesthesiologist_notes == "My reasons were y"

        updated4_case3 = update_questionnaire(questionnaire3.id, user_type=doctor.type, doctor_status="approved_w_c", operation_date=datetime(2023, 1, 1))
        assert updated4_case3 is not None
        assert updated4_case3.doctor_status == "approved_w_c"
        assert updated4_case3.operation_date == date(2023, 1, 1)

        # Case 4 - Anesthesiologist approves, doctor declines with clarification -> patient
        updated_case4 = update_questionnaire(questionnaire3.id, user_type=anesthesiologist.type, status="approved")
        assert updated_case4 is not None
        assert updated_case4.status == "approved"

        updated2_case4 = update_questionnaire(questionnaire3.id, user_type=doctor.type, doctor_status="declined_w_c_p", doctor_notes="My reasons were x")
        assert updated2_case4 is not None
        assert updated2_case4.doctor_status == "declined_w_c_p"
        assert updated2_case4.doctor_notes == "My reasons were x"

        updated3_case4 = update_questionnaire(questionnaire3.id, user_type=patient.type, patient_notes="My reasons were y")
        assert updated3_case4 is not None
        assert updated3_case4.doctor_status == "declined_w_c_p"
        assert "My reasons were y" in updated3_case4.patient_notes  

        updated4_case4 = update_questionnaire(questionnaire3.id, user_type=anesthesiologist.type, status="approved", anesthesiologist_notes="My reasons were y")
        assert updated4_case4 is not None
        assert updated4_case4.status == "approved"
        assert updated4_case4.anesthesiologist_notes == "My reasons were y"

        updated5_case5 = update_questionnaire(questionnaire3.id, user_type=doctor.type, doctor_status="approved_w_c", operation_date=datetime(2023, 1, 1))
        assert updated5_case5 is not None
        assert updated5_case5.doctor_status == "approved_w_c"
        assert updated5_case5.operation_date == date(2023, 1, 1)

