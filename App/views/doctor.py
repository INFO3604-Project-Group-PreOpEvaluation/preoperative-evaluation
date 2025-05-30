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
    
    personal_notifications = get_user_notifications(current_user.type, current_user.id)
    # Retrieve all patient questionnaires from the database
    patient_questionnaires = get_all_questionnaires()

    # Render the dashboard template with the retrieved data
    return render_template('doctor_dashboard.html', patient_questionnaires=patient_questionnaires, patients=patients, notifications=personal_notifications)

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
    status = data['doctor_status']

    # Print the data for debugging purposes
    # print(questionnaire_id, operation_date, notes, status)
    
    # Update the questionnaire in the database
    updated = update_questionnaire(questionnaire_id, user_type="doctor", operation_date=operation_date, doctor_notes=notes, doctor_status=status)
    questionnaire = get_questionnaire_by_id(questionnaire_id)
    patient = get_patient_by_id(questionnaire.patient_id)
        # Send a notification to the Doctor
    if status == "approved" or status == "approved_w_c": 
        notif = create_notification(patient_id=patient.id, message=f"Doctor {current_user.firstname} {current_user.lastname} has approved your questionnaire. See your dashboard for more details", title="Success")

    elif status == "declined" or status == "denied_w_c":
        # Send a notification to the patient
        notif = create_notification(patient_id=patient.id, message=f"Your questionnaire has been declined by Doctor {current_user.firstname} {current_user.lastname}, please resubmit or contact the doctor", title="Error")

    if updated:
        # Flash a success message if the update is successful
        flash('Notes added successfully')
    else:
        # Flash an error message if the update fails
        flash('Error adding notes')
    
    # Redirect back to the previous page
    return redirect(url_for('doctor_views.doctor_dashboard_page'))
