from App.models import Anesthesiologist
from App.models import db
from sqlalchemy.exc import IntegrityError

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
        db.session.rollback()
        print(e, "Error creating anesthesiologist")
        
        return None


def get_anesthesiologist_by_email(anesthesiologist_email):
    # Query the database for anesthesiologist by email
    anesthesiologist = Anesthesiologist.query.filter_by(email=anesthesiologist_email).first()
    try:
        anesthesiologist = Anesthesiologist.query.filter_by(email=anesthesiologist_email).first()
    except Exception as e:
        # Print the error message if an exception occurs
        print(e, "Error getting anesthesiologist by email") 
        return None

    return anesthesiologist

