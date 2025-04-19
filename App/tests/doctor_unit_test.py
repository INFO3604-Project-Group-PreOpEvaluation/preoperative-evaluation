import pytest
import unittest
from App.models import Doctor
from App.controllers import (
    create_doctor
)

'''
    Unit Tests
'''

class DoctorUnitTests(unittest.TestCase):
    """
    Unit tests for the Doctor model and its respective controller functions.
    """
    def test_new_doctor(self):
        """
        A Doctor object is created and contains all fields from the input.
        """
        doctor = Doctor(firstname="John", lastname="Doe", password="securepassword", email="john.doe@example.com", phone_number="1234567890")
        self.assertIsNotNone(doctor)
        self.assertEqual(doctor.firstname, "John")
        self.assertEqual(doctor.lastname, "Doe")
        self.assertEqual(doctor.email, "john.doe@example.com")
        self.assertEqual(doctor.phone_number, "1234567890")

    def test_doctor_to_json(self):
        """
        A Doctor object is created and its to_json method is called.
        """
        doctor = Doctor(firstname="John2", lastname="Doe2", password="password123", email="john.doe@example.com", phone_number="1234567890")
        doctor_json = doctor.get_json()


        # Test that the returned dictionary values match the Doctor object's attributes
        self.assertIsNotNone(doctor_json['id'])
        self.assertEqual(doctor_json['firstname'], doctor.firstname)
        self.assertEqual(doctor_json['lastname'], doctor.lastname)
        self.assertEqual(doctor_json['email'], doctor.email)
        self.assertEqual(doctor_json['phone_number'], doctor.phone_number)
        self.assertEqual(doctor_json['type'], doctor.type)

    # Test that to_json method handles special characters correctly
    

    def test_doctor_missing_fields(self):
        """
        Verify that creating a Doctor without required fields raises errors.
        """
        with self.assertRaises(ValueError) as context:  
            new_doctor = Doctor(firstname=None, lastname=None,
                                  password=None, email=None, phone_number=None)
            self.assertEqual(str(context), "All fields for a doctor are required.")

    def test_doctor_to_json_special_characters(self):
        """
        Verify that to_json() handles special characters correctly.
        """
        doctor_special = Doctor(firstname="Jöhn", lastname="Döe", password="p@ssword123", email="john!doe@example.com", phone_number="+1 (123) 456-7890")
        doctor_special_json = doctor_special.get_json()
        self.assertEqual(doctor_special_json['firstname'], "Jöhn")
        self.assertEqual(doctor_special_json['lastname'], "Döe")
        self.assertEqual(doctor_special_json['email'], "john!doe@example.com")
        self.assertEqual(doctor_special_json['phone_number'], "+1 (123) 456-7890")

    def test_doctor_password_security(self):
        """
        Verify that passwords meet security requirements.
        """
        new_doctor = Doctor(
            firstname="Secure", 
            lastname="User", 
            password="sTr0ngP@ssw0rd", 
            email="secure.user@example.com", 
            phone_number="0123456789"
        )

        assert len(new_doctor.password) >= 8  # Example: Enforce length
        assert any(char.isupper() for char in new_doctor.password)  # Example: Enforce uppercase
        assert any(char.islower() for char in new_doctor.password)  # Example: Enforce lowercase
        assert any(char.isdigit() for char in new_doctor.password)  # Example: Enforce digit

