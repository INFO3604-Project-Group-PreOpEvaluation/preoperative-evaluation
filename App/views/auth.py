from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
# from flask_jwt_extended import jwt_required# current_user as jwt_current_user
# from flask_login import login_required, login_user, current_user, logout_user
from App.models import db, Patient, Anesthesiologist, Doctor
from App.controllers import *

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page Routes
'''

@auth_views.route('/signin', methods=['GET'])
def signin_page():
  return render_template('signin.html')

@auth_views.route('/signup', methods=['GET'])
def signup_page():
  return render_template('signup.html')



'''
Action Routes
'''

@auth_views.route('/signin', methods = ['POST'])
def signin_action():
    print("\n=== SIGNIN ACTION DEBUG ===")
    data = request.form
    email = data.get('email')
    password = data.get('password')
    
    print(f"Attempting login for email: {email}")
    
    if not email or not password:
        print("✗ Missing email or password")
        flash('Email and password are required')
        return redirect(url_for('auth_views.signin_page'))
    
    # Try to login each user type
    user = None
    
    # Try Patient first
    print("\nTrying patient login...")
    patient = Patient.query.filter_by(email=email).first()
    if patient:
        print(f"Found patient: {patient.email}")
        if patient.check_password(password):
            user = login_patient(email, password)
            if user:
                print(f"✓ Successfully logged in as patient: {patient.email}")
                return redirect(url_for('patient_views.patient_profile_page'))
            else:
                print("✗ Patient login failed")
        else:
            print("✗ Patient password verification failed")
    else:
        print("✗ No patient found with that email")
    
    # Try Anesthesiologist
    print("\nTrying anesthesiologist login...")
    anesthesiologist = Anesthesiologist.query.filter_by(email=email).first()
    if anesthesiologist:
        print(f"Found anesthesiologist: {anesthesiologist.email}")
        if anesthesiologist.check_password(password):
            user = login_anesthesiologist(email, password)
            if user:
                print(f"✓ Successfully logged in as anesthesiologist: {anesthesiologist.email}")
                return redirect(url_for('anesthesiologist_views.anesthesiologist_dashboard_page'))
            else:
                print("✗ Anesthesiologist login failed")
        else:
            print("✗ Anesthesiologist password verification failed")
    else:
        print("✗ No anesthesiologist found with that email")
    
    # Try Doctor last
    print("\nTrying doctor login...")
    doctor = Doctor.query.filter_by(email=email).first()
    if doctor:
        print(f"Found doctor: {doctor.email}")
        if doctor.check_password(password):
            user = login_doctor(email, password)
            if user:
                print(f"✓ Successfully logged in as doctor: {doctor.email}")
                return redirect(url_for('doctor_views.doctor_dashboard_page'))
            else:
                print("✗ Doctor login failed")
        else:
            print("✗ Doctor password verification failed")
    else:
        print("✗ No doctor found with that email")
    
    flash('Invalid email or password')
    return redirect(url_for('auth_views.signin_page'))

@auth_views.route('/signup', methods=['POST'])
def signup_action():
  
  try:
    data = request.form     
    print(data)   
    patient = create_patient(firstname=data['firstname'], lastname=data['lastname'], password = data['password'], email=data['email'], phone_number=data['phone_number'])
    login_user(patient)

    if patient:
      flash('Account Created!')  
      return redirect("/patient/profile") 

  except Exception as e:      
    print("Error in signup: ", e)
    flash("Username, Email, or UWI ID already exist")  # error message
    return redirect(url_for('auth_views.signup_page'))


@auth_views.route('/identify', methods=['GET'])
def identify_page():
    print("\n=== IDENTIFY PAGE DEBUG ===")
    if current_user.is_authenticated:
        print(f"Current user details:")
        print(f"Email: {current_user.email}")
        print(f"Type: {getattr(current_user, 'type', 'unknown')}")
        print(f"ID: {current_user.id}")
        print(f"Class: {type(current_user).__name__}")
        return jsonify({'message': f"{current_user.get_json()}"}) 
    print("No user logged in")
    return jsonify({'message': "Not Logged In"})

  
@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout()
    flash('Logged Out!')
    return redirect('/')

'''
API Routes
'''


@auth_views.route('/api/signin', methods=['POST'])
def user_login_api():
  data = request.json
  logout_user()

  if not data or 'email' not in data or 'password' not in data:
        return jsonify(error='Missing email or password'), 400

  user_credentials = jwt_authenticate(data['email'], data['password'])

  if not user_credentials:
    return jsonify(error='invalid credentials'), 400

  access_token = create_access_token(identity=user_credentials)
  return jsonify(access_token=access_token), 200

@auth_views.route('/api/signup', methods=['POST'])
def user_signup_api():
    print("tt")
    data = request.json
    print(data)
    if not data or 'email' not in data or 'password' not in data:
        return jsonify(error='Missing email or password'), 400

    try:
        user = create_patient(firstname=data['firstname'], lastname=data['lastname'], password = data['password'], email=data['email'], phone_number=data['phone_number'])
        if user:
            access_token = create_access_token(identity=user.email)
            return jsonify(message="Account Created"), 201
    except IntegrityError:
        return jsonify(error='Account already exists'), 400

