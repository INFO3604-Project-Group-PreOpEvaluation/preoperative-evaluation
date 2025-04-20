from App.models import Doctor
from App.database import db
from App.controllers.notification import create_notification
from sqlalchemy.exc import IntegrityError

def create_doctor(firstname, lastname,password, email, phone_number):
    """
    Creates a new doctor object in the database.

    Returns:
    Doctor: The newly created doctor object if successful, None otherwise.
    """
    try:
        # Create a new Doctor object
        new_doctor = Doctor(firstname=firstname, lastname=lastname,  password=password, email=email, phone_number=phone_number)
        
        # Add the new doctor to the database session
        db.session.add(new_doctor)
        
        # Commit the session to save the doctor to the database
        db.session.commit()
        
        # Return the newly created doctor
        return new_doctor
    except IntegrityError as e:
        raise IntegrityError(None, None, "Integrity error while creating doctor") from e
    except Exception as e:
        # Print the error message if an exception occurs
        db.session.rollback()
        print(e, "Error creating doctor")
        # Return None to indicate failure
        return None
    

def get_doctor_by_email(doctor_email):
    # Query the database for doctor by email
    try:
        doctor = Doctor.query.filter_by(email=doctor_email).first()
    except Exception as e:
        # Print the error message if an exception occurs
        print(e, "Error getting doctor by email") 
        return None

    return doctor

