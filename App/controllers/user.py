from App.models import User
from App.database import db



def createUser(username, password, email):
    newuser = User(username = username, password= password, email= email)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def get_user(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def check_username_password(username, password):
    user = User.query.filter_by(username=username).first()
    return user and user.check_password(password)

    
        


    