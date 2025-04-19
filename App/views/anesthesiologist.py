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
    print("TESTTSTA")
    try:
        # Get all the questionnaires that have been submitted
        patient_questionnaires = get_all_questionnaires()
        # Get all the patients
        patients = get_all_patients()
    except Exception as e:
        print(e, "Error getting patient questionnaires and patients")
    return render_template('anesthesiologist_dashboard.html', patient_questionnaires=patient_questionnaires, patients=patients)


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
    if update_questionnaire_anesthesiologist(current_user.id, questionnaire_id, notes, status):
        flash('Notes added successfully')
    else:
        flash('Error adding notes')
    # Redirect to the previous page
    return redirect(request.referrer)


