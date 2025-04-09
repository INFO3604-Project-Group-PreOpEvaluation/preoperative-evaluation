from App.models import db
from App.controllers.patient import create_patient
from App.controllers.doctor import create_doctor
from App.controllers.anesthesiologist import create_anesthesiologist



def initialize_db():
    try:
        db.drop_all()
        db.create_all()   
        patient = create_patient(firstname= 'John', lastname='Doe', password='password', phone_number='1234567890', email='johndoe@mail.com')
        doctor = create_doctor(firstname='Jane', lastname='Doe',  password='password', email= 'janedoe@mail.com', phone_number='0987654321' )
        anesthesiologist = create_anesthesiologist(firstname='Mike', lastname='Smith', password='password', phone_number='1122334455', email='mikesmith@mail.com')
        db.session.commit()
        print('Database initialised successfully')

    except Exception as e:
        db.session.rollback()
        print(f"Error initialising database: {e}")


