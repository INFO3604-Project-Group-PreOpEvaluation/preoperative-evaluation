from App.database import db
from .user import User
from .questionnaire import Questionnaire

class Anesthesiologist(User):
    """
    Represents an anesthesiologist user in the database.

    In addition to the standard User fields, an anesthesiologist has a
    type field set to 'anesthesiologist'.
    """
    __tablename__ = 'anesthesiologist'
    type = db.Column(db.String(120), nullable=False, default='anesthesiologist')

    def __init__(self, firstname, lastname, username, password, email, phone_number):
        """
        Constructor for Anesthesiologist.

        """
        super().__init__(firstname, lastname, username, password, email, phone_number)
        self.type = 'anesthesiologist'

    def get_json(self):
        """
        Return a JSON representation of the Anesthesiologist.

        :return: JSON representation of the Anesthesiologist
        """
        return{
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'username': self.username,
            'email': self.email,
            'phone_number': self.phone_number,
            'type': self.type
        }
    
    def update_questionnaire_anesthesiologist(self, questionnaire_id, new_anesthesiologist_notes, status):
        """
        Updates the anesthesiologist's notes and status for a given questionnaire.
        :return: The updated questionnaire
        """
        questionnaire = Questionnaire.query.get(questionnaire_id)
        if questionnaire:
            try:
                questionnaire.anesthesiologist_notes = new_anesthesiologist_notes
                if questionnaire.status == 'denied_w_c' and status == 'approved':
                    questionnaire.status = 'approved_w_c'
                else:
                    questionnaire.status = status
                db.session.commit()
                return questionnaire
            except Exception as e:
                import logging
                logging.error("Error updating anesthesiologist notes: %s", e)
                return None         
        return None

    