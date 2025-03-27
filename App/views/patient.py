from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from App.models import db
from App.controllers import *


patient_views = Blueprint('patient_views', __name__, template_folder='../templates')


'''
Page Routes
'''

@patient_views.route('/patient/profile', methods=['GET'])
@patient_required
def patient_profile_page():
    """
    View for the patient's profile page

    This route renders the patient_account.html template with the patient's
    notifications.

    :return: The rendered template
    """
    try:
        # Get all the notifications for the current user
        notifications = get_patient_notifications(current_user.id)

        # If the medical history has not been updated, display a warning message
        if not current_user.med_history_updated:
            flash('Please update your Medical History to be able to fill out a questionnaire')

        # Render the template
        return render_template('patient_account.html', notifications=notifications)

    except Exception as e:
        # Print any errors that occur
        print("Patient Profile View Error: ", str(e))



'''
Action Routes
'''

@patient_views.route('/patient/medical_history', methods=['POST'])
def add_medical_history_action():
    """
    Add a patient's medical history

    This route handles the POST request from the patient's profile page
    to add their medical history.

    :return: A redirect to the patient's profile page with a success or error message
    """
    try:
        # Get the data from the form submission
        data = request.form
        age = data['age']
        blood_type = data['blood_type']
        weight = data['weight']
        height = data['height']
        allergies = data['allergies']
        medical_conditions = data['medical_conditions']
        medication = data['medication']

        # Add the medical history to the database
        if create_medical_history(current_user.id, age, blood_type, weight, height, allergies, medical_conditions, medication):
            flash('Medical history added successfully')
        else:
            flash('Error adding medical history')

        # Redirect back to the patient's profile page
        return redirect(request.referrer)
    except Exception as e:
        # Print the error to the console
        print("Patient Medical History View Error: ",str(e))




@patient_views.route('/seen/<notification_id>', methods=['POST'])
@patient_required
def seen_action(notification_id):
    """
    Mark a notification as seen
    :param notification_id: The ID of the notification to mark as seen
    :return: A JSON response indicating if the notification was marked as seen
    """
    try:
        # Call the seen_notification function to mark the notification as seen
        response = seen_notification(notification_id)
        if response:
            # Return a JSON response with a success message
            return jsonify({'message': 'Notification seen'})
        # Return a JSON response with an error message
        return jsonify({'message': 'Notification not seen'}), 400
    except Exception as e:
        # Print any errors that occur
        print("Patient Notification View Error: ",str(e))

