from flask_login import login_user, login_manager, logout_user, LoginManager, current_user
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
from flask import render_template, redirect, url_for, flash
from flask import session

from App.models import User, Doctor, Anesthesiologist, Patient

from functools import wraps


def jwt_authenticate(username, password):
    user = Patient.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)
    
    user = Doctor.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)

    user = Anesthesiologist.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)

    return None

def login(username, password):
    user = Patient.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)

    user = Doctor.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)

    user = Anesthesiologist.query.filter_by(username=username).first()
  
    if user and user.check_password(password):
        return create_access_token(identity=username)
    return None

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        print("\n=== USER LOADER DEBUG ===")
        print(f"Attempting to load user with ID: {user_id}")
        
        # First, try to find the user in each table and verify their type
        for model in (Doctor, Patient, Anesthesiologist):
            print(f"\nTrying to load from {model.__name__} table...")
            user = model.query.get(user_id)
            if user:
                print(f"Found user in {model.__name__} table:")
                print(f"Email: {user.email}")
                print(f"Type: {type(user).__name__}")
                print(f"Current type attribute: {getattr(user, 'type', 'not set')}")
                
                # Double check that this is the correct user type
                if isinstance(user, Doctor) and model == Doctor:
                    user.type = 'doctor'
                    print("✓ Confirmed as doctor")
                    return user
                elif isinstance(user, Patient) and model == Patient:
                    user.type = 'patient'
                    print("✓ Confirmed as patient")
                    return user
                elif isinstance(user, Anesthesiologist) and model == Anesthesiologist:
                    user.type = 'anesthesiologist'
                    print("✓ Confirmed as anesthesiologist")
                    return user
                else:
                    print(f"✗ Type mismatch! Expected {model.__name__}, got {type(user).__name__}")
        
        print("\nNo matching user found in any table")
        return None
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        # Try to find the user in each model
        for model in (Doctor, Patient, Anesthesiologist):
            user = model.query.filter_by(email=identity).first()
            if user:
                return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        # Try to find the user in each model
        for model in (Doctor, Patient, Anesthesiologist):
            user = model.query.get(identity)
            if user:
                # Set the type attribute based on the model
                user.type = model.__tablename__
                return user
        return None

    return jwt

    #Edits below

#Login actions
def login_anesthesiologist(email, password):
    print("\n=== ANESTHESIOLOGIST LOGIN DEBUG ===")
    print(f"Attempting to login anesthesiologist with email: {email}")
    
    anesthesiologist = Anesthesiologist.query.filter_by(email=email).first()
    if anesthesiologist:
        print(f"Found anesthesiologist: {anesthesiologist.email}")
        print(f"Type: {type(anesthesiologist).__name__}")
        
        if anesthesiologist.check_password(password):
            print("Password verified")
            anesthesiologist.type = 'anesthesiologist'
            login_user(anesthesiologist)
            print(f"Successfully logged in anesthesiologist: {anesthesiologist.email}")
            return anesthesiologist
        else:
            print("- Password verification failed")
    else:
        print("- No anesthesiologist found with that email")
    return None

def login_doctor(email, password):
    print("\n=== DOCTOR LOGIN DEBUG ===")
    print(f"Attempting to login doctor with email: {email}")
    
    doctor = Doctor.query.filter_by(email=email).first()
    if doctor:
        print(f"Found doctor: {doctor.email}")
        print(f"Type: {type(doctor).__name__}")
        
        if doctor.check_password(password):
            print("Password verified")
            doctor.type = 'doctor'
            login_user(doctor)
            print(f"Successfully logged in doctor: {doctor.email}")
            return doctor
        else:
            print("- Password verification failed")
    else:
        print("- No doctor found with that email")
    return None

def login_patient(email, password):
    print("\n=== PATIENT LOGIN DEBUG ===")
    print(f"Attempting to login patient with email: {email}")
    
    patient = Patient.query.filter_by(email=email).first()
    if patient:
        print(f"Found patient: {patient.email}")
        print(f"Type: {type(patient).__name__}")
        
        if patient.check_password(password):
            print("Password verified")
            patient.type = 'patient'
            login_user(patient)
            print(f"Successfully logged in patient: {patient.email}")
            return patient
        else:
            print("- Password verification failed")
    else:
        print("- No patient found with that email")
    return None

def logout():
    logout_user()
    return True

#Wrappers
def anesthesiologist_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Checking anesthesiologist access. User authenticated: {current_user.is_authenticated}, Type: {getattr(current_user, 'type', 'unknown')}")
        if not current_user.is_authenticated:
            return redirect(url_for('auth_views.signin_page'))
        if not hasattr(current_user, 'type') or current_user.type != 'anesthesiologist':
            print(f"Access denied. User type: {getattr(current_user, 'type', 'unknown')}")
            flash('You do not have permission to access this page')
            return redirect(url_for('index_views.index_page'))
        return func(*args, **kwargs)
    return wrapper

def doctor_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Checking doctor access. User authenticated: {current_user.is_authenticated}, Type: {getattr(current_user, 'type', 'unknown')}")
        if not current_user.is_authenticated:
            return redirect(url_for('auth_views.signin_page'))
        if not hasattr(current_user, 'type') or current_user.type != 'doctor':
            print(f"Access denied. User type: {getattr(current_user, 'type', 'unknown')}")
            flash('You do not have permission to access this page')
            return redirect(url_for('index_views.index_page'))
        return func(*args, **kwargs)
    return wrapper

def patient_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):        
        print(f"Checking patient access. User authenticated: {current_user.is_authenticated}, Type: {getattr(current_user, 'type', 'unknown')}")
        if not current_user.is_authenticated:
            return redirect(url_for('auth_views.signin_page'))
        if not hasattr(current_user, 'type') or current_user.type != 'patient':
            print(f"Access denied. User type: {getattr(current_user, 'type', 'unknown')}")
            flash('You do not have permission to access this page')
            return redirect(url_for('index_views.index_page'))
        return func(*args, **kwargs)
    return wrapper

# Context processor to make 'is_authenticated' available to all templates
def add_auth_context(app):
    @app.context_processor
    def inject_user():
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            current_user = User.query.get(user_id)
            is_authenticated = True
            # current_user = None
            # for model in [Doctor, Anesthesiologist, Patient]:
            #     user = model.query.get(user_id)
            #     if user:
            #         current_user = user
            #         break
            # is_authenticated = bool(current_user)

        except Exception as e:
            print(e)
            is_authenticated = False
            current_user = None
        return dict(is_authenticated=is_authenticated, current_user=current_user)