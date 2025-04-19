import pytest
import unittest
from datetime import datetime
from App.main import create_app
from App.database import db, create_db
from App.models import Anesthesiologist
from App.controllers import (
    create_anesthesiologist,
    update_questionnaire_anesthesiologist

)

'''
    Unit Tests
'''
class AnesthesiologistUnitTests(unittest.TestCase):
    """
    Unit tests for the Anesthesiologist model.

    These tests verify that the Anesthesiologist model is correctly
    created and that the to_json() method is working correctly.
    """

    def test_new_anesthesiologist(self):
        """
        Verify that a new Anesthesiologist object can be created
        and that the fields are correctly set.
        """
        newAnesthiologist = Anesthesiologist(
            firstname="John1",
            lastname="Doe1",
            password="password1231",
            email="cT2oB@example.com1",
            phone_number="1234567890"
        )
        assert newAnesthiologist is not None
        assert newAnesthiologist.firstname == "John1"
        assert newAnesthiologist.lastname == "Doe1"
        assert newAnesthiologist.email == "cT2oB@example.com1"
        assert newAnesthiologist.phone_number == "1234567890"
        assert newAnesthiologist.type == "anesthesiologist"

    def test_anesthesiologist_to_json(self):
        """
        Verify that to_json() works correctly.
        """
        # Create a new Anesthesiologist instance
        newAnesthesiologist = Anesthesiologist(
            firstname="John2",
            lastname="Doe2",
            password="password123",
            email="john.doe@example.com",
            phone_number="1234567890"
        )
        
        # Generate JSON and expected output
        anesthesiologist_json = newAnesthesiologist.get_json()
        
        # Test the JSON structure
        self.assertDictEqual(anesthesiologist_json, {
            "id": None, 
            "firstname": "John2",
            "lastname": "Doe2",
            "email": "john.doe@example.com",
            "phone_number": "1234567890",
            "type": "anesthesiologist"
        })
    
    def test_anesthesiologist_missing_fields(self):
        """
        Verify that creating an Anesthesiologist without required fields raises errors.
        """
        with self.assertRaises(ValueError) as context:  
            newAnesthesiologist = Anesthesiologist(firstname=None, lastname=None,
                                                   password=None, email=None, phone_number=None)
            self.assertEqual(str(context), "All fields for an anesthesiologist are required.")
            # self.assertTrue('All fields are required.' in str(context.exception))
            # self.assertTrue('All fields are required.' == str(context))
    def test_anesthesiologist_to_json_special_characters(self):
        """
        Verify that to_json() handles special characters correctly.
        """
        newAnesthesiologist = Anesthesiologist(
            firstname="Jöhn", lastname="Döe", password="p@ssword123",
            email="john!doe@example.com", phone_number="+1 (123) 456-7890"
        )

        anesthesiologist_json = newAnesthesiologist.get_json()

        self.assertEqual(anesthesiologist_json['firstname'], "Jöhn")
        self.assertEqual(anesthesiologist_json['lastname'], "Döe")
        self.assertEqual(anesthesiologist_json['email'], "john!doe@example.com")
        self.assertEqual(anesthesiologist_json['phone_number'], "+1 (123) 456-7890")
        

    def test_anesthesiologist_password_security(self):
        """
        Verify that passwords meet security requirements.
        """
        newAnesthesiologist = Anesthesiologist(
            firstname="Secure", lastname="User",
            password="sTr0ngP@ssw0rd",
            email="secure.user@example.com", phone_number="0123456789"
        )

        assert len(newAnesthesiologist.password) >= 8  # Example: Enforce length
        assert any(char.isupper() for char in newAnesthesiologist.password)  # Example: Enforce uppercase
        assert any(char.islower() for char in newAnesthesiologist.password)  # Example: Enforce lowercase
        assert any(char.isdigit() for char in newAnesthesiologist.password)  # Example: Enforce digit