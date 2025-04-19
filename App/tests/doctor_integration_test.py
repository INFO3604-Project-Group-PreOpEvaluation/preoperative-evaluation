import pytest
import unittest
from App.main import create_app
from App.database import db, create_db
from sqlalchemy.exc import IntegrityError

from App.controllers import (
    create_doctor
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

class DoctorIntegrationTests(unittest.TestCase):
    '''
        Integration Tests for the Doctor model and Controller

        These tests ensure that the Doctor model and controller
        functions behave as expected. They cover the following scenarios:

        - Creating a new Doctor
        - Creating a new Doctor with a duplicate email or username
    '''

    def test_create_doctor(self):
        '''
            Test that a new Doctor can be created successfully
        '''
        new_doctor = create_doctor("John", "Smith","password", "johnsmith@mail.com", "1234567890")
        assert new_doctor is not None
        assert new_doctor.firstname == "John"
        assert new_doctor.lastname == "Smith"
        assert new_doctor.phone_number == "1234567890"
        assert new_doctor.email == "johnsmith@mail.com"

    def test_duplicate_email_or_username(self):
        '''
            Test that attempting to create an Doctor with a duplicate
            email or username results in the expected behavior
        '''
        # Create an Doctor to create a duplicate of
        create_doctor("Jane", "Doe", "password", "janedoe@mail.com", "0987654321")

        # Attempt to create an Doctor with the same email
        with self.assertRaises(IntegrityError) as context:  # Or another appropriate exception
            newDoctor = create_doctor("Alice", "Smith", "password", "janedoe@mail.com", "1122334455")
            self.assertIn("Integrity error while creating doctor", str(context.exception))
