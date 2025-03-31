import pytest
import unittest
from datetime import datetime
from App.main import create_app
from App.database import db, create_db
from App.models import Anesthesiologist, Questionnaire
from App.controllers import (
    create_anesthesiologist,
    update_questionnaire_anesthesiologist
)

'''
    Integration Tests
'''

@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()

class AnesthiologistIntegrationTests(unittest.TestCase):
    '''
        Integration Tests for the Anesthesiologist model and Controller

        These tests ensure that the Anesthesiologist model and controller
        functions behave as expected. They cover the following scenarios:

        - Creating a new Anesthesiologist
        - Creating a new Anesthesiologist with a duplicate email or username
    '''

    def test_create_anesthesiologist(self):
        '''
            Test that a new Anesthesiologist can be created successfully
        '''
        new_anesthesiologist = create_anesthesiologist("John", "Smith", "johnsmith", "password", "johnsmith@mail.com", "1234567890")
        assert new_anesthesiologist is not None
        assert new_anesthesiologist.firstname == "John"
        assert new_anesthesiologist.lastname == "Smith"
        assert new_anesthesiologist.username is not None
        assert new_anesthesiologist.phone_number == "1234567890"
        assert new_anesthesiologist.email == "johnsmith@mail.com"

    def test_duplicate_email_or_username(self):
        '''
            Test that attempting to create an Anesthesiologist with a duplicate
            email or username results in the expected behavior
        '''
        # Create an Anesthesiologist to create a duplicate of
        create_anesthesiologist("Jane", "Doe", "janedoe", "password", "janedoe@mail.com", "0987654321")

        # Attempt to create an Anesthesiologist with the same email
        duplicate_email = create_anesthesiologist("Alice", "Smith", "alice", "password", "janedoe@mail.com", "1122334455")

        # Attempt to create an Anesthesiologist with the same username
        duplicate_username = create_anesthesiologist("Bob", "Brown", "janedoe", "password", "bob@mail.com", "6677889900")

        # Assert that the duplicates were not created
        assert duplicate_email is None  # Assuming function returns None for duplicates
        assert duplicate_username is None
