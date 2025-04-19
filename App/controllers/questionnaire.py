from App.models import Questionnaire
from datetime import datetime
from App.database import db
from App.controllers.patient import set_patient_autofill_enabled
from datetime import datetime
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


def update_questionnaire(questionnaire_id, user_type ,**kwargs):

    """
    Update a questionnaire in the database with the given ID.

    Args:
    questionnaire_id (str): The ID of the questionnaire to update.
    **kwargs: Keyword arguments to update the questionnaire with.

    Returns:
    Questionnaire: The updated questionnaire object if successful, None otherwise.
    """
    try:
        # Retrieve the questionnaire from the database
        questionnaire = get_questionnaire(questionnaire_id)

        
        # If questionnaire exists, append the new notes to existing ones
        if questionnaire:
            if questionnaire.status == "declined":
                return questionnaire
            # Check if the user is a doctor or anesthesiologist
            
            if user_type == 'doctor':
                try:
                    # Update the doctor_notes field
                    questionnaire.doctor_notes = kwargs.get('doctor_notes', '')
                    questionnaire.doctor_status = kwargs.get('doctor_status', 'pending')
                    operation_date = kwargs.get('operation_date', '')
                    print(operation_date, "- operation_date")
                    if isinstance(operation_date, str):
                        questionnaire.operation_date = datetime.strptime(operation_date, '%Y-%m-%d').date()
                    elif isinstance(operation_date, datetime):
                        questionnaire.operation_date = operation_date.date()
                    
                except Exception as e:
                    # Print the error message if an exception occurs
                    print(e, "Error updating doctor notes")
            elif user_type == 'anesthesiologist':
                try:
                    # Update the anesthesiologist_notes field
                    questionnaire.anesthesiologist_notes = kwargs.get('anesthesiologist_notes', '')
                    questionnaire.status = kwargs.get('status', 'pending')

                except Exception as e:
                    # Print the error message if an exception occurs
                    print(e, "Error updating anesthesiologist notes")
                    return None
            else:
                try:
                    # Get existing notes or empty string if None
                    existing_notes = questionnaire.patient_notes or ""
                    
                    # Get new notes from kwargs
                    new_notes = kwargs.get('patient_notes', '')

                    # Get existing status
                    status = questionnaire.status
                    
                    # If status is not 'denied_w_c', don't allow updates
                    # if status != 'denied_w_c':
                    #     return None
                    
                    # Append new notes with timestamp
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    updated_notes = f"{existing_notes}\n[{timestamp}] {new_notes}".strip()
                    
                    # Update the questionnaire
                    questionnaire.patient_notes = updated_notes

                except Exception as e:
                    # Print the error message if an exception occurs
                    print(e, "Error updating patient notes")
                    return None
            db.session.commit()
            
            return questionnaire        
        return None
    except Exception as e:
        # Print the error message if an exception occurs
        print(e, "Error updating questionnaire")

        raise Exception("Error updating questionnaire")
        
        return None
        
    

#     questionnaire = Questionnaire.query.get(questionnaire_id)
#     if not questionnaire:
#         return None
#     try:
#         for key, value in kwargs.items():
#             if hasattr(questionnaire, key):
#                 setattr(questionnaire, key, value)
#         db.session.commit()
#         return questionnaire
#     except Exception as e:
#         # Print the error message if an exception occurs
#         db.session.rollback()
#         print(e, "Error updating questionnaire")
#         return None

