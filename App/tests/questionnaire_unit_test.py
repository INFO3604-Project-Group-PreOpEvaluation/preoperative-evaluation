import os, tempfile, pytest, logging, unittest
from werkzerg.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Questionnaire
from App.controllers import(
    create_questionnaire,
    get_questionnaire,
    get_all_questionnaires,
    get_all_questionnaires_json,
    get_questionnaire_by_patient_id,
    get_questionnaire_by_status,
    get_questionnaire_by_status_json,
    get_latest_questionnaire
)

class QuestionnaireUnitTests(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_get_questionnaire(self):
        patient_id = "patient123"
        responses = {"q1": "yes", "q2": "no"}
        created = create_questionnaire(patient_id, responses)
        retrieved = get_questionnaire(created.id)
        self.assertEqual(created.id, retrieved.id)

    def test_get_all_questionnaires(self):
        patient_id_1 = "patient123"
        patient_id_2 = "patient456"
        create_questionnaire(patient_id_1, {"q1": "yes"})
        create_questionnaire(patient_id_2, {"q2": "no"})
        questionnaires = get_all_questionnaires()
        self.assertEqual(len(questionnaires), 2)
