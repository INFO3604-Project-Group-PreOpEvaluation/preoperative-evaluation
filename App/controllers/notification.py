from flask import Blueprint, jsonify, request
from App.database import db
from App.models import Notification
from datetime import datetime

def create_notification(patient_id, anesthesiologist_id, doctor_id, message, title):
    """
    Creates a new notification

    Args:
        patient_id (str): The id of the patient this notification is for
        anesthesiologist_id (str): The id of the anesthesiologist this notification is for
        doctor_id (str): The id of the doctor this notification is for
        message (str): The message of the notification
        title (str): The title of the notification

    Returns:
        Notification: The newly created notification
    """
    try:
        new_notification = Notification(patient_id=patient_id, anesthesiologist_id=anesthesiologist_id, doctor_id=doctor_id, message=message, title=title)
        db.session.add(new_notification)
        db.session.commit()
        return new_notification
    except Exception as e:
        print(e)
        db.session.rollback()
        return None    
    

def get_notifications_json():
    """
    Retrieves all notifications in the database as json

    Returns:
        json: A json object containing all notifications
    """
    notifications = Notification.query.all()
    notifications_list = [notification.get_json() for notification in notifications]
    return jsonify({'notifications': notifications_list})

def get_notifications():
    """
    Retrieves all notifications in the database

    Returns:
        list: A list of all notifications
    """
    notifications = Notification.query.all()
    return notifications

def get_notification(notification_id):
    """
    Retrieves a notification by its id

    Args:
        notification_id (int): The id of the notification to retrieve

    Returns:
        json: A json object containing the notification
    """
    notification = Notification.query.get_or_404(notification_id)
    return jsonify(notification.get_json())
     
def delete_notification(notification_id):
    """
    Deletes a notification by its id

    Args:
        notification_id (int): The id of the notification to delete

    Returns:
        json: A json object indicating whether the notification was deleted successfully
    """
    notification = Notification.query.get(notification_id)
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404

    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Notification deleted successfully'})


def get_user_notifications(user_type, user_id):
    """
    Retrieves all notifications for a user

    Args:
        user_type (str): The type of user (patient, anesthesiologist, doctor)
        user_id (str): The id of the user to retrieve notifications for

    Returns:
        list: A list of all notifications for the user
    """
    if user_type == 'patient':
        user_notifications = Notification.query.filter_by(patient_id=user_id, seen=False).order_by(Notification.timestamp.desc()).all()
    elif user_type == 'anesthesiologist':
        user_notifications = Notification.query.filter_by(anesthesiologist_id=user_id, seen=False).order_by(Notification.timestamp.desc()).all()
    elif user_type == 'doctor':
        user_notifications = Notification.query.filter_by(doctor_id=user_id, seen=False).order_by(Notification.timestamp.desc()).all()
    else:
        return jsonify({'error': 'User type not supported'}), 400
    
    notification_info = []

    for notification in user_notifications:
        info = notification.get_json()

        time_ago = (datetime.now() - notification.timestamp).total_seconds()
        if time_ago < 60:
            info['time_ago'] = f"{int(time_ago)}s"
        elif time_ago < 3600:
            info['time_ago'] = f"{int(time_ago // 60)}m"
        elif time_ago < 86400:
            info['time_ago'] = f"{int(time_ago // 3600)}h"
        elif time_ago < 604800:
            info['time_ago'] = f"{int(time_ago // 86400)}d"
        elif time_ago < 2629800:
            info['time_ago'] = f"{int(time_ago // 604800)}w"
        elif time_ago < 31557600:
            info['time_ago'] = f"{int(time_ago // 2629800)}mo"
        else:
            info['time_ago'] = f"{int(time_ago // 31557600)}y"
            
        notification_info.append(info)
    return notification_info
      

def seen_notification(notification_id):
    """
    Marks a notification as seen

    Args:
        notification_id (int): The id of the notification to mark as seen

    Returns:
        bool: Whether the notification was found and marked as seen
    """
    notification = Notification.query.get(notification_id)
    if not notification:
        return False        #verifying notification exists 

    notification.seen = True
    db.session.commit()
    return True
