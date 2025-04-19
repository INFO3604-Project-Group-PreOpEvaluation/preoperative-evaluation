from App.models import Questionnaire
from App.database import db
from App.controllers.patient import set_patient_autofill_enabled

def create_questionnaire(patient_id, responses):
    """
    Create a new questionnaire for a patient and save it to the database.

    Parameters:
    patient_id (str): The ID of the patient the questionnaire is associated with.
    responses (dict): A dictionary containing the responses to the questionnaire questions.

    Returns:
    Questionnaire: The newly created questionnaire object if successful, None otherwise.
    """
    try:
        # Create a new Questionnaire object
        new_questionnaire = Questionnaire(patient_id=patient_id, responses=responses)
        
        # Add the new questionnaire to the database session
        db.session.add(new_questionnaire)
        
        # Commit the session to save the questionnaire to the database
        db.session.commit()
        
        # Enable autofill for the patient
        set_patient_autofill_enabled(patient_id, True)
        
        return new_questionnaire
    except Exception as e:
        # Print the error message if an exception occurs
        print(e, "Error creating questionnaire")
        
        return None
    
def get_questionnaire(id):
    """
    Retrieve a questionnaire from the database by its ID.

    Parameters:
    id (int): The ID of the questionnaire to retrieve.

    Returns:
    Questionnaire: The questionnaire with the given ID if it exists, None otherwise.
    """
    return Questionnaire.query.get(id)

def get_all_questionnaires():
    """
    Retrieve all questionnaires from the database.

    Returns:
    list: A list of all Questionnaire objects in the database.
    """
    return Questionnaire.query.all()

def get_all_questionnaires_json():
    """
    Retrieve all questionnaires from the database and return them as JSON.

    Returns:
    list: A list of JSON objects, each containing the details of a questionnaire.
    """
    # Retrieve all questionnaires from the database
    questionnaires = Questionnaire.query.all()
    
    # If no questionnaires are found, return an empty list
    if not questionnaires:
        return []
    
    # Convert each questionnaire to JSON
    questionnaires = [questionnaire.get_json() for questionnaire in questionnaires]
    
    # Return the list of JSON objects
    return questionnaires

def get_questionnaire_by_patient_id(patient_id):
    """
    Retrieve a questionnaire from the database by its patient's ID.

    Parameters:
    patient_id (int): The ID of the patient whose questionnaire to retrieve.

    Returns:
    Questionnaire: The questionnaire for the given patient if it exists, None otherwise.
    """
    return Questionnaire.query.filter_by(patient_id=patient_id).first()

def get_questionnaire_by_status(status):
    """
    Retrieve all questionnaires from the database with the given status.

    Args:
    status (str): The status of the questionnaires to retrieve.

    Returns:
    list: A list of all Questionnaire objects in the database with the given status.
    """
    return Questionnaire.query.filter_by(status=status).all()

def get_questionnaire_by_status_json(status):
    """
    Retrieve all questionnaires from the database with the given status and return them as JSON.

    Args:
    status (str): The status of the questionnaires to retrieve.

    Returns:
    list: A list of JSON objects, each containing the details of a questionnaire.
    """
    # Retrieve all questionnaires from the database with the given status
    questionnaires = Questionnaire.query.filter_by(status=status).all()
    
    # If no questionnaires are found, return an empty list
    if not questionnaires:
        return []
    
    # Convert each questionnaire to JSON
    questionnaires = [questionnaire.get_json() for questionnaire in questionnaires if questionnaire is not None]
    
    # Return the list of JSON objects
    return questionnaires

def get_latest_questionnaire(patient_id):
    """
    Retrieve the latest questionnaire from the database for the given patient.

    Args:
    patient_id (str): The ID of the patient to retrieve the questionnaire for.

    Returns:
    Questionnaire: The latest questionnaire for the given patient if it exists, None otherwise.
    """
    # Retrieve the latest questionnaire from the database for the given patient
    latest_questionnaire = Questionnaire.query.filter_by(patient_id=patient_id).order_by(Questionnaire.submitted_date.desc()).first()
    
    # If no questionnaire is found, return None
    if latest_questionnaire is None:
        return None
    
    # Return the latest questionnaire
    return latest_questionnaire

def update_questionnaire(questionnaire_id, **kwargs):
    """
    Update a questionnaire in the database.

    Parameters:
    questionnaire_id (int): The ID of the questionnaire to update.
    **kwargs: Keyword arguments representing the fields to update in the questionnaire.

    Returns:
    Questionnaire: The updated questionnaire object if successful, None otherwise.
    """
    questionnaire = Questionnaire.query.get(questionnaire_id)
    if not questionnaire:
        return None
    try:
        for key, value in kwargs.items():
            if hasattr(questionnaire, key):
                setattr(questionnaire, key, value)
        db.session.commit()
        return questionnaire
    except Exception as e:
        # Print the error message if an exception occurs
        db.session.rollback()
        print(e, "Error updating questionnaire")
        return None
