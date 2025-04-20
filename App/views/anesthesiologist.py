from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db
from App.controllers import *

anesthesiologist_views = Blueprint('anesthesiologist_views', __name__, template_folder='../templates')


'''
Page Routes
'''

@anesthesiologist_views.route('/dashboard/anesthesiologist', methods=['GET'])
@anesthesiologist_required
def anesthesiologist_dashboard_page():
    """
    Anesthesiologist's dashboard page.
    
    Returns:
        render_template(str, dict): The dashboard page with all the patient's questionnaires.
    """
    try:
        # Get all the questionnaires that have been submitted
        patient_questionnaires = get_all_questionnaires()
        personal_notifications = get_user_notifications(current_user.type, current_user.id)
        # Get all the patients
        patients = get_all_patients()
    except Exception as e:
        print(e, "Error getting patient questionnaires and patients")
    return render_template('anesthesiologist_dashboard.html', patient_questionnaires=patient_questionnaires, patients=patients, notifications=personal_notifications)


@anesthesiologist_views.route('/dashboard/anesthesiologist/patient/<patient_id>', methods=['GET'])
@anesthesiologist_required
def anesthesiologist_patient_info_page(patient_id):
    """
    Render the patient information page for a specific patient.

    Returns:
        Response: The rendered template for the patient information page.
    """
    # Retrieve patient details using the provided patient ID
    patient = get_patient_by_id(patient_id)
    
    # Render the patient info template with the retrieved patient data
    return render_template('patient_info.html', patient=patient)

@anesthesiologist_views.route('/dashboard/anesthesiologist/questionnaire/<questionnaire_id>', methods=['GET'])
@anesthesiologist_required
def anesthesiologist_questionnaire_page(questionnaire_id):
    """
    Render the questionnaire page for the given questionnaire ID.

    Returns:
        Response: The rendered template for the questionnaire page.
    """
    # Get the questionnaire that matches the provided questionnaire ID
    questionnaire = get_questionnaire(questionnaire_id)
    # Retrieve the default questionnaire
    questions = get_default_questionnaire()
    # Render the questionnaire template with the retrieved questionnaire and default questions
    return render_template('questionnaire_view.html', questionnaire=questionnaire, questions=questions)


'''
Action Routes
'''

@anesthesiologist_views.route('/dashboard/anesthesiologist/questionnaire/submit/<questionnaire_id>', methods=['POST'])
@anesthesiologist_required
def update_questionnaire_anesthesiologist_action(questionnaire_id):
    """
    Update the questionnaire with the anesthesiologist's notes and status.

    :return: A redirect to the previous page.
    """
    data = request.form   
    status = data['status']
    notes = data['anesthesiologist_notes']
    print(questionnaire_id, status, notes)

    # Update the questionnaire with the anesthesiologist's notes and status
    updated = update_questionnaire(questionnaire_id, user_type="anesthesiologist", anesthesiologist_notes=notes, status=status)

    # Send a notification to the Doctor
    if status == "approved" or status == "approved_w_c":
        doctor = get_doctor_by_email("janedoe@mail.com") # hardcoded as only one doctor
        notif = create_notification(doctor_id=doctor.id, message="A patient has been approved", title="Success")

    elif status == "declined" or status == "denied_w_c":
        questionnaire = get_questionnaire_by_id(questionnaire_id)

        # Send a notification to the patient
        patient = get_patient_by_id(questionnaire.patient_id)
        notif = create_notification(patient_id=patient.id, message="Your questionnaire has been declined, please resubmit or contact the anesthesiologist", title="Error")
    if updated:
        flash('Notes added successfully')
    else:
        flash('Error adding notes')
    # Redirect to the previous page
    return redirect(url_for('anesthesiologist_views.anesthesiologist_dashboard_page'))


