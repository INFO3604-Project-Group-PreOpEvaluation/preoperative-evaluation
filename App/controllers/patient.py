from App.database import db
from App.models import Patient
import uuid
def generate_short_uuid():
        return str(uuid.uuid4())[:10]
def create_patient(firstname, lastname, username, password, email, phone_number):
    """
    Creates a new patient in the database
    
    Parameters:
    firstname (str): The patient's first name
    lastname (str): The patient's last name
    username (str): The patient's username
    password (str): The patient's password
    email (str): The patient's email
    phone_number (str): The patient's phone number
    
    Returns:
    Patient: The newly created patient
    """
    uname = generate_short_uuid()
    try:
        new_patient = Patient(firstname=firstname, lastname=lastname, username=uname, password=password, email=email, phone_number=phone_number)
        db.session.add(new_patient)
        db.session.commit()
        return new_patient
    except Exception as e:
        print(e, "Error creating patient")
        return None

def create_medical_history(patient_id, age, blood_type, weight, height, allergies, medical_conditions, medication):
    """
    Creates a new medical history for the patient in the database
    
    Parameters:
    patient_id (str): The id of the patient
    age (int): The patient's age
    blood_type (str): The patient's blood type
    weight (float): The patient's weight
    height (float): The patient's height
    allergies (str): The patient's allergies
    medical_conditions (str): The patient's medical conditions
    medication (str): The patient's medication
    
    Returns:
    Patient: The patient with the updated medical history
    """
    patient = Patient.query.get(patient_id)
    try:
        # Update the patient's medical history
        patient.age = age
        patient.blood_type = blood_type
        patient.weight = weight
        patient.height = height
        patient.allergies = allergies
        patient.medical_conditions = medical_conditions
        patient.medication = medication
        patient.med_history_updated = True        
        # Save the changes to the database
        db.session.commit()
        return patient
    except Exception as e:
        # If there is an error, print the error and return None
        print(e, "Error creating medical history")
        return None
    
def get_all_patients():
    """
    Returns all patients in the database

    Returns:
    list: A list of all Patient objects in the database
    """
    return Patient.query.all()

def get_patient_by_id(patient_id):
    """
    Returns a patient with the given id from the database

    Parameters:
    patient_id (str): The id of the patient to retrieve

    Returns:
    Patient: The patient with the given id, or None if no such patient exists
    """
    return Patient.query.get(patient_id)

def set_patient_autofill_enabled(patient_id, status):
    """
    Sets the autofill_enabled status of a patient to the given value

    Parameters:
    patient_id (str): The id of the patient to set
    status (bool): The new value for the autofill_enabled status

    Returns:
    bool: True if the status was successfully set, False otherwise
    """
    patient = Patient.query.get(patient_id)
    if patient.autofill_enabled == status:
        # If the status is already set to the desired value, return True
        return True
    try:
        # Set the autofill_enabled status and save the changes to the database
        patient.autofill_enabled = status
        db.session.commit()
        return True
    except Exception as e:
        # If there is an error, print the error and return False
        print(e, "Error setting autofill status")
        return False
