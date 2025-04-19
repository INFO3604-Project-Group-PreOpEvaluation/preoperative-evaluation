from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db
from App.controllers import *
import datetime


doctor_views = Blueprint('doctor_views', __name__, template_folder='../templates')

'''
Page Routes
'''


@doctor_views.route('/dashboard/doctor', methods=['GET'])
@doctor_required
def doctor_dashboard_page():
    """
    Render the doctor's dashboard page with patient and questionnaire data.

    This route is only accessible to authenticated users with a doctor role. It retrieves
    all patients and questionnaires from the database and passes them to the template for rendering.

    Returns:
        str: The rendered HTML for the doctor's dashboard page.
    """
    # Retrieve all patients from the database
    patients = get_all_patients()
    
    # Retrieve all patient questionnaires from the database
    patient_questionnaires = get_all_questionnaires()

    # Render the dashboard template with the retrieved data
    return render_template('doctor_dashboard.html', patient_questionnaires=patient_questionnaires, patients=patients)

@doctor_views.route('/dashboard/doctor/patient/<patient_id>', methods=['GET'])
@doctor_required
def doctor_patient_info_page(patient_id):
    """
    Render the doctor's patient information page with patient data.

    This route is only accessible to authenticated users with a doctor role. It retrieves
    a patient by ID from the database and passes it to the template for rendering.

    Returns:
        str: The rendered HTML for the doctor's patient information page.
    """
    # Retrieve the patient by ID from the database
    patient = get_patient_by_id(patient_id)
    
    # Render the patient information template with the retrieved data
    return render_template('patient_info.html', patient=patient)

@doctor_views.route('/dashboard/doctor/questionnaire', methods=['GET'])
@doctor_required
def doctor_questionnaire_page():
    """
    Render the doctor's questionnaire page with questionnaire data.

    This route is only accessible to authenticated users with a doctor role. It retrieves
    a questionnaire by ID from the database and passes it to the template for rendering.

    Returns:
        str: The rendered HTML for the doctor's questionnaire page.
    """
    # Retrieve the questionnaire ID from the URL parameters
    questionnaire_id = request.args.get('questionnaire_id')

    # Retrieve the questionnaire by ID from the database
    questionnaire = get_questionnaire(questionnaire_id)

    # Retrieve the default questionnaire questions from the database
    questions = get_default_questionnaire()

    # Render the questionnaire template with the retrieved data
    return render_template('questionnaire_view.html', questionnaire=questionnaire, questions=questions)


'''
Action Routes
'''

@doctor_views.route('/dashboard/doctor/questionnaire/submit/<questionnaire_id>', methods=['POST'])
def update_questionnaire_doctor_action(questionnaire_id):
    """
    Route to handle the submission of the doctor's notes and operation date for a questionnaire.

    This route is only accessible to authenticated users with a doctor role. It retrieves
    the operation date and notes from the submitted form data, updates the questionnaire
    in the database, and redirects back to the previous page.

    Returns:
        Response: A redirect response back to the previous page.
    """
    # Retrieve the form data
    data = request.form
    
    # Retrieve the operation date and notes from the form data
    operation_date = data['operation_date']
    notes = data['doctor_notes']

    # Print the data for debugging purposes
    print(questionnaire_id, operation_date, notes)
    
    # Update the questionnaire in the database
    if update_questionnaire(current_user.id, questionnaire_id, notes, operation_date):
        # Flash a success message if the update is successful
        flash('Notes added successfully')
    else:
        # Flash an error message if the update fails
        flash('Error adding notes')
    
    # Redirect back to the previous page
    return redirect(request.referrer)
