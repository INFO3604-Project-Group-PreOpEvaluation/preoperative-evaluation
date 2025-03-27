from App.models import Doctor
from App.database import db
from App.controllers.notification import create_notification

def create_doctor(firstname, lastname, username, password, email, phone_number):
    """
    Creates a new doctor object in the database.

    Returns:
    Doctor: The newly created doctor object if successful, None otherwise.
    """
    try:
        # Create a new Doctor object
        new_doctor = Doctor(firstname=firstname, lastname=lastname, username=username, password=password, email=email, phone_number=phone_number)
        
        # Add the new doctor to the database session
        db.session.add(new_doctor)
        
        # Commit the session to save the doctor to the database
        db.session.commit()
        
        # Return the newly created doctor
        return new_doctor
    except Exception as e:
        # Print the error message if an exception occurs
        print(e, "Error creating doctor")
        
        # Return None to indicate failure
        return None
    

def update_questionnaire_doctor(doctor_id, questionnaire_id, new_doctor_notes, new_operation_date):
    # Verify the doctor's existence and authority
    doctor = Doctor.query.get(doctor_id)
    if doctor:        
        questionnaire = doctor.update_questionnaire_doctor(questionnaire_id, new_doctor_notes, new_operation_date)
        if questionnaire:
            notification = create_notification(questionnaire.patient_id, f"Doctor {doctor.lastname} has reviewed your questionnaire", "Questionnaire Updated")
            return True
        else:
            return False
    else:
        return False  # Doctor not found or not authorized