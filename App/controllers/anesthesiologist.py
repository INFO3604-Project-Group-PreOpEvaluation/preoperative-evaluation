from App.models import Anesthesiologist
from App.models import db
from sqlalchemy.exc import IntegrityError
from App.controllers.notification import create_notification

def create_anesthesiologist(firstname, lastname, password, email, phone_number):
    """
    Create a new anesthesiologist and save them to the database.

    Returns:
    Anesthesiologist: The newly created anesthesiologist object if successful, None otherwise.
    """
    try:
        # Create a new Anesthesiologist object
        new_anesthesiologist = Anesthesiologist(
            firstname=firstname,
            lastname=lastname,
            password=password,
            email=email,
            phone_number=phone_number
        )
        
        # Add the new anesthesiologist to the database session
        db.session.add(new_anesthesiologist)
        
        # Commit the session to save the anesthesiologist to the database
        db.session.commit()
        
        return new_anesthesiologist
    except IntegrityError as e:
        raise IntegrityError(None, None, "Integrity error while creating anesthesiologist") from e
    except Exception as e:
        # Print the error message if an exception occurs
        print(e, "Error creating anesthesiologist")
        
        return None

def update_questionnaire_anesthesiologist(anesthesiologist_id, questionnaire_id, new_anesthesiologist_notes, status):
    """
    Updates the anesthesiologist's notes and status for a questionnaire.

    Returns:
    bool: True if the questionnaire was updated successfully, False otherwise.
    """
    # Verify the anesthesiologist's existence and authority
    anesthesiologist = Anesthesiologist.query.get(anesthesiologist_id)
    if anesthesiologist:
        # Call the method on the anesthesiologist object to update the questionnaire
        questionnaire = anesthesiologist.update_questionnaire_anesthesiologist(questionnaire_id, new_anesthesiologist_notes, status)
        if questionnaire:
            # Create a new notification for the patient about the questionnaire update
            notification = create_notification(questionnaire.patient_id, f"Anesthesiologist {anesthesiologist.lastname} has reviewed your questionnaire", "Questionnaire Updated")
            # Return True to indicate the questionnaire was updated successfully
            return True
        else:
            # Return False if the questionnaire was not updated successfully
            return False
    else:
        # Return False if the anesthesiologist was not found or not authorized
        return False
