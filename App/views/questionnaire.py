from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, url_for, flash
from App.models import db
from App.controllers import *

questionnaire_views = Blueprint('questionnaire_views', __name__, template_folder='../templates')


@questionnaire_views.route('/questionnaire', methods=['GET', 'POST'])
@patient_required
def questionnaire_page():
    """
    Handles rendering the questionnaire form for a patient.

    If the patient has not updated their medical history, redirect them to the patient profile page.
    Otherwise, render the questionnaire form with the questionnaire questions and the latest responses
    if the patient has autofill enabled.
    """
    questions = get_default_questionnaire()
    if not current_user.med_history_updated:
        flash('Please update your medical history before taking the questionnaire')
        return redirect(url_for('patient_views.patient_profile_page'))
    latest_responses = None
    if current_user.autofill_enabled:
        latest_responses = get_latest_questionnaire(current_user.id).responses
    return render_template('questionnaire_form.html', questions=questions, latest_responses=latest_responses)

@questionnaire_views.route('/questionnaire/details', methods=['GET', 'POST'])
@patient_required
def questionnaire_details_page():
    """
    Handles rendering the questionnaire details page for a patient.

    If the questionnaire ID is not found in the request, flash an error message and redirect the patient to the questionnaire page.
    If the questionnaire ID is invalid, flash an error message and redirect the patient to the questionnaire page.
    Otherwise, render the questionnaire details page with the questionnaire questions and the given questionnaire.
    """
    questionnaire_id = request.args.get('questionnaire_id')
    if not questionnaire_id:
        # If the questionnaire ID is not found in the request, flash an error message
        flash('Questionnaire ID not found')
        return redirect(url_for('questionnaire_views.questionnaire_page'))
    questionnaire = get_questionnaire(questionnaire_id)
    if not questionnaire:
        # If the questionnaire ID is invalid, flash an error message
        flash('Invalid questionnaire ID')
        return redirect(url_for('questionnaire_views.questionnaire_page'))
    questions = get_default_questionnaire()
    return render_template('questionnaire_view.html', questions=questions, questionnaire=questionnaire)


@questionnaire_views.route('/submit_questionnaire', methods=['POST'])
@patient_required
def submit_questionnaire():
    """
    Handles the submission of the questionnaire form.

    Parses the form data, constructs a responses dictionary, 
    processes follow-up questions, and saves the responses 
    to the database.
    
    Returns:
    A rendered template of the questionnaire view page with
    the submitted responses, or flashes an error message if 
    the submission fails.
    """
    # Retrieve the default set of questions
    questions = get_default_questionnaire()

    # Parse form data to build the responses dictionary
    responses = {}
    for key, value in request.form.items():
        if key.startswith('question_'):
            # Extract question ID from form field
            question_id = key.split('_')[1]
            responses[question_id] = value

    # Process follow-up questions if any
    for question in questions:
        if question.get('follow_ups'):
            for follow_up in question['follow_ups']:
                follow_up_id = 'question_' + follow_up['id']
                if follow_up_id in request.form:
                    responses[follow_up['id']] = request.form[follow_up_id]

    # Save the responses to the database
    questionnaire = create_questionnaire(patient_id=current_user.id, responses=responses)
    
    # Flash appropriate message based on success or failure
    if questionnaire:
        flash('Questionnaire submitted successfully!')
    else:
        flash('Error submitting questionnaire! Please try again')
    anes = get_anesthesiologist_by_email('mikesmith@mail.com') # hardcoded as only one anesthesiologist 
    notif = create_notification(anesthesiologist_id=anes.id, message="Patient has submitted their questionnaire", title="New Questionnaire Submission")
    
    return redirect(url_for('questionnaire_views.questionnaire_details_page', questionnaire_id=questionnaire.id))


@questionnaire_views.route('/questionnaire/update_notes', methods=['POST'])
@patient_required
def update_questionnaire_notes():
    notes = request.form.get('patient_notes')
    if not notes:
        flash('No notes provided')
        return redirect(url_for('questionnaire_views.questionnaire_details_page'))

    updated = update_questionnaire(current_user.id, current_user.type, patient_notes=notes)
    
    if updated:
        flash('Notes updated successfully!')
    else:
        flash('Error updating notes')
    anes = get_anesthesiologist_by_email('mikesmith@mail.com') # hardcoded as only one anesthesiologist 
    notif = create_notification(anesthesiologist_id=anes.id, message="Patient has submitted notes for their questionnaire", title="New Questionnaire Notes")
        
    return redirect(url_for('patient_views.patient_profile_page'))

