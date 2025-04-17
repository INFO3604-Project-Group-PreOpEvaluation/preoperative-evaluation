import click, pytest, sys
from flask import Flask, render_template
from flask.cli import with_appcontext, AppGroup
import os

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import *

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

def run_command():
    os.system("npm install tailwindcss @tailwindcss/cli")
    os.system("npx @tailwindcss/cli -i App/static/Css/input.css -o App/static/Css/output.css")

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    run_command()    
    initialize_db()


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 



# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_patients())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

patient_cli = AppGroup('patient', help='Patient object commands')


app.cli.add_command(patient_cli)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))


@test.command("anes", help="Run Anesthesiologist tests")
@click.argument("type", default="all")
def anesthesiologist_tests_command(type):
  if type == "unit":
    sys.exit(pytest.main(["-k", "AnesthesiologistUnitTests"]))
  elif type == "int":
    sys.exit(pytest.main(["-k", "AnesthesiologistIntegrationTests"]))
  else:
    sys.exit(pytest.main(["-k", "Anesthesiologist"]))


@test.command("patient", help="Run Patient Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "PatientUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "PatientIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Patient"]))

@test.command("question", help="Run Questionnaire Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "QuestionnaireUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "QuestionnaireIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Question"]))

@test.command("doctor", help="Run Doctor Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "DoctorUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "DoctorIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Doctor"]))

@test.command("notif", help="Run Notification Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "NotificationUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "NotificationIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Notification"]))


app.cli.add_command(test)