<h1 align="center">
  <img src="images/logo0.png" alt="PreOp Logo" />
</h1>

<div align="center">

[![Python IDLE](https://img.shields.io/badge/Python%20IDLE-3776AB?logo=python&logoColor=fff)](#)
[![CSS](https://img.shields.io/badge/CSS-1572B6?logo=css3&logoColor=fff)](#)
[![HTML](https://img.shields.io/badge/HTML-%23E34F26.svg?logo=html5&logoColor=white)](#)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=000)](#)
[![Visual Studio Code](https://custom-icon-badges.demolab.com/badge/Visual%20Studio%20Code-0078d7.svg?logo=vsc&logoColor=white)](#)
[![Trello](https://img.shields.io/badge/Trello-0052CC?logo=trello&logoColor=fff)](#)
[![Postgres](https://img.shields.io/badge/Postgres-%23316192.svg?logo=postgresql&logoColor=white)](#)
[![Flask](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff)](#)
[![Website](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](https://preoperative-evaluation-9t5i.onrender.com/)

</div>

# **🏥 Preoperative Evaluation System ⚕️**

## **📜 Overview**

The increasing demands placed on public healthcare institutions, particularly in preoperative assessment, underscore the need for innovative solutions that enhance efficiency, accuracy, and patient-centred care. This project introduces a **web-based “Preoperative Evaluation” system** 💻 designed to **modernize and streamline surgical preparation**  within public healthcare institutions. The system aims to enhance **efficiency, accuracy, and patient-centered care ❤** by facilitating the **digital submission  and review  of preoperative questionnaires**. This allows patients to securely provide their medical histories and receive timely evaluations from anesthesiologists.

The platform facilitates efficient communication  and coordination among **patients, anesthesiologists, and doctors** by enabling the **electronic submission, review, and approval of preoperative questionnaires**. It reduces reliance on paper-based forms , minimizes administrative delays, and ensures healthcare professionals can make informed decisions based on accessible and structured patient data .

The system facilitates secure registration and authentication of users, allowing patients to create profiles and submit detailed medical histories through a structured preoperative questionnaire. Once submitted, anesthesiologists receive notifications to review the information, add evaluative notes, and determine whether the patient is medically fit to proceed with surgery. Only after approval by the anesthesiologist can doctors access the relevant patient records, review them, and proceed to schedule surgical appointments.
The website lacked security implementations, so encryption was added to secure patient data. The project implemented AES-GCM to ensure both confidentiality and data integrity for patients. This method was chosen due to its strong security guarantees and efficiency.

## **🛠️ Technologies Used**

The Preoperative Evaluation system utilizes the following technologies:

*   **💻 Flask:** Web framework for backend development.
*   **🐍Python:** Programming language.
*   **🎨 Bootstrap:** Front-end framework for responsive and user-friendly interface design.
*   **🌐 HTML & CSS:** Markup and styling languages for the user interface.
*   **☁️ Render:** Cloud-based hosting platform for deployment.
*   **🐘 PostgreSQL:** Relational database management system for secure data storage.
*   **🔗 SQLAlchemy:** Flask's built-in Object Relational Mapper (ORM) for database interaction using Python.
*   **🏛️ Flask MVC template:** Used for structuring the application.
*   **🧑‍💻 GitHub & Gitpod:** Development tools for collaboration, version control, cloud-based development, testing, and code editing.

## **🚀 Deployment**

The deployed application can be accessed at: **[https://preoperative-evaluation-9t5i.onrender.com/](https://preoperative-evaluation-9t5i.onrender.com/)** 🔗.

## **🧪 Testing**

The project underwent various levels of testing to ensure functionality and reliability:

*   **✅ User Acceptance Tests (UAT):** Conducted for patients, anesthesiologists, and doctors to validate key workflows such as signup, login, questionnaire submission/review, and appointment scheduling.
*   **🧩 Unit Tests:** Focused on testing individual components (models) of the system, such as patient, anesthesiologist, doctor, questionnaire, and notification models, to ensure they function as expected.


*   **🔗 Integration Tests:** Aimed at verifying the interaction and data flow between different parts of the system, ensuring that components work correctly together.

# Application overview

## **🔑 Key Features**

### **🧑‍⚕️ Patients**

![Patient](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcWV0ZzN0NDlkd2RwcWhybHhwN2V2dzVhNWd5a2gwbGE1cnowcDRsaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xlPCzuWGPXgdpdYfVI/giphy.gif)

*   **🔒 Secure Registration and Authentication:** Patients can securely register and log in to the system.
*   **👤 Profile Management:** Patients can create and manage their profiles.
*   **📝 Medical History Submission:** Patients can submit detailed medical histories through a structured online questionnaire.
*   **⏱️ Questionnaire Status Tracking:** Patients can view the status and progress of their submitted questionnaires.
*   **🔔 Notification System:** Patients receive real-time alerts regarding the status of their questionnaire.
*   **💬 Communication:** Patients can communicate with both doctors and anesthesiologists.
*   **📅 View Operation Date:** Patients can view their assigned operation date once approved.


---


### **👩‍⚕️ Anesthesiologists**

![Anesthesiologist](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExMngzaHgzcDJwcnM0MzM0cnFzZ2pwaHBsdXU4aHplbGJrNGszcHVyZiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/pHGkgiXWOBYm1yCqOG/giphy.gif)

*   **🔒 Secure Login and Authentication:** Anesthesiologists can securely log in to the system.
*   **🧑‍⚕️ Patient Management:** Anesthesiologists can view a list of their assigned patients.
*   **📜 Medical History Review:** Anesthesiologists can view the medical history of their assigned patients.
*   **🧐 Questionnaire Review and Approval:** Anesthesiologists can view patient questionnaire results, add evaluative notes ✍️, and approve 👍 or deny 👎 them based on medical assessments.
*   **🔔 Notification System:** Anesthesiologists receive notifications for incoming patient questionnaires.
*   **💬 Communication:** Anesthesiologists can communicate with both doctors and patients.



---

### **👨‍⚕️ Doctors**

![Doctor](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2ZsbmJ1cjN6bmw4cG04ZXgyOHF3N3I1ODU5M2o2MWZyeHJkZGNrciZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/oIHYvVUPGDrHUsFdoN/giphy.gif)

*   **🔒 Secure Login and Authentication:** Doctors can securely log in to the system.
*   **🧑‍⚕️ Patient Management:** Doctors can view a list of their assigned patients.
*   **✅ Access to Approved Records:** Doctors can access only those patient records and questionnaires that have been approved by the anesthesiologist.
*   **📜 Medical History Review:** Doctors can view the medical history of their patients.
*   **✅ Questionnaire Review:** Doctors can view the anesthesiologist-approved patient questionnaires.
*   **✍️ Note Taking:** Doctors can leave notes for approved questionnaires.
*   **🗓️ Appointment Scheduling:** Doctors can approve 👍/deny 👎 patients for surgery and schedule surgical appointments.
*   **💬 Communication:** Doctors can communicate with both anesthesiologists and patients.


---


[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/INFO3604-Project-Group-PreOpEvaluation/preoperative-evaluation)

## Deploy to Render
<a href="https://render.com/deploy?repo=https://github.com/uwidcit/flaskmvc">
  <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
</a>

---

### Useful:

https://github.com/inttter/md-badges


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt


# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Flask Commands

wsgi.py is a utility script for performing various tasks related to the project. You can use it to import and test any code in the project. 
You just need create a manager command function, for example:

```python
# inside wsgi.py

user_cli = AppGroup('user', help='User object commands')

@user_cli.cli.command("create-user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

app.cli.add_command(user_cli) # add the group to the cli

```

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command. This must also be executed once when running the app on heroku by opening the heroku console, executing bash and running the command in the dyno.

```bash
$ flask init
```

# Running the Project

_For development run the serve command (what you execute):_
```bash
$ flask run
```

_For production using gunicorn (what heroku executes):_
```bash
$ gunicorn wsgi:app
```

# Testing

## Unit & Integration
Unit and Integration tests are created in the App/test. You can then create commands to run them. Look at the unit test command in wsgi.py for example:

```python
@test.command("patient", help="Run Patient Tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "PatientUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "PatientIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "Patient"]))
```

You can then execute all user tests as follows

```bash
$ flask test patient
```

You can also supply "unit" or "int" at the end of the comand to execute only unit or integration tests. For example:

```bash
$ flask test patient unit
$ flask test patient int
```

You can run all application tests with the following command

```bash
$ pytest
```
# Troubleshooting

## Views 404ing

If your newly created views are returning 404 ensure that they are added to the list in main.py.

```python
from App.views import (
    user_views,
    index_views
)

# New views must be imported and added to this list
views = [
    user_views,
    index_views
]
```

# Configuration Management


Configuration information such as the database url/port, credentials, API keys etc are to be supplied to the application. However, it is bad practice to stage production information in publicly visible repositories.
Instead, all config is provided by a config file or via [environment variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/).

## In Development

When running the project in a development environment (such as gitpod) the app is configured via default_config.py file in the App folder. By default, the config for development uses a sqlite database.

default_config.py
```python
SQLALCHEMY_DATABASE_URI = "sqlite:///temp-database.db"
SECRET_KEY = "secret key"
JWT_ACCESS_TOKEN_EXPIRES = 7
ENV = "DEVELOPMENT"
```

These values would be imported and added to the app in load_config() function in config.py

config.py
```python
# must be updated to inlude addtional secrets/ api keys & use a gitignored custom-config file instad
def load_config():
    config = {'ENV': os.environ.get('ENV', 'DEVELOPMENT')}
    delta = 7
    if config['ENV'] == "DEVELOPMENT":
        from .default_config import JWT_ACCESS_TOKEN_EXPIRES, SQLALCHEMY_DATABASE_URI, SECRET_KEY
        config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
        config['SECRET_KEY'] = SECRET_KEY
        delta = JWT_ACCESS_TOKEN_EXPIRES
...
```

## In Production

When deploying your application to production/staging you must pass
in configuration information via environment tab of your render project's dashboard.

![perms](./images/fig1.png)
