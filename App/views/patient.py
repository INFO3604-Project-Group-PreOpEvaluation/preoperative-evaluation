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
        notifications = get_user_notifications(current_user.type, current_user.id)

        # If the medical history has not been updated, display a warning message
        if not current_user.med_history_updated:
            flash('Please update your Medical History to be able to fill out a questionnaire')

        # Render the template
        return render_template('patient_account.html', notifications=notifications)

    except Exception as e:
    # Print any errors that occur
        print("Patient Profile View Error: ", str(e))
    return jsonify({'error': 'An error occurred'}), 500



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
        dateOfBirth = data['dateOfBirth']
        blood_type = data['blood_type']
        weight = data['weight']
        height = data['height']
        allergies = data['allergies']
        medical_conditions = data['medical_conditions']
        medication = data['medication']

        # Add the medical history to the database
        if create_medical_history(current_user.id, dateOfBirth, blood_type, weight, height, allergies, medical_conditions, medication):
            flash('Medical history added successfully')
        else:
            flash('Error adding medical history')

        # Redirect back to the patient's profile page
        return redirect(request.referrer)
    except Exception as e:
        # Print the error to the console
        print("Patient Medical History View Error: ",str(e))
        return redirect(request.referrer)




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

"""

API Routes

"""

@patient_views.route('/api/patient/profile', methods=['GET'])
@jwt_required()
def api_patient_profile():
    """
    API route for fetching the patient's profile data.

    :return: A JSON response with patient profile data and notifications
    """
    try:
        notifications = get_user_notifications(current_user.type, current_user.id)
        profile_data = {
            'firstname': current_user.firstname,
            'lastname': current_user.lastname,
            'email': current_user.email,
            'dateOfBirth': current_user.dateOfBirth,
            'blood_type': current_user.blood_type,
            'weight': current_user.weight,
            'height': current_user.height,
            'allergies': current_user.allergies,
            'medical_conditions': current_user.medical_conditions,
            'medication': current_user.medication,
            'notifications': notifications
        }
        return jsonify(profile_data), 200
    except Exception as e:
        print("API Patient Profile Error: ", str(e))
        return jsonify({'error': 'An error occurred'}), 500

@patient_views.route('/api/patient/medical_history', methods=['POST'])
# @jwt_required()
def api_add_medical_history():
    """
    API route for adding a patient's medical history

    :return: A JSON response with a success or error message
    """
    try:
        data = request.json
        dateOfBirth = data.get('dateOfBirth')
        blood_type = data.get('blood_type')
        weight = data.get('weight')
        height = data.get('height')
        allergies = data.get('allergies')
        medical_conditions = data.get('medical_conditions')
        medication = data.get('medication')

        if create_medical_history(current_user.id, dateOfBirth, blood_type, weight, height, allergies, medical_conditions, medication):
            return jsonify({'message': 'Medical history added successfully'}), 200
        else:
            return jsonify({'error': 'Error adding medical history'}), 400
    except Exception as e:
        print("API Medical History Error: ", str(e))
        return jsonify({'error': 'An error occurred'}), 500

@patient_views.route('/api/seen/<notification_id>', methods=['POST'])
@jwt_required()
def api_seen_notification(notification_id):
    """
    API route for marking a notification as seen

    :param notification_id: The ID of the notification
    :return: A JSON response indicating success or failure
    """
    try:
        response = seen_notification(notification_id)
        if response:
            return jsonify({'message': 'Notification seen'}), 200
        return jsonify({'message': 'Notification not seen'}), 400
    except Exception as e:
        print("API Notification Error: ", str(e))
        return jsonify({'error': 'An error occurred'}), 500

