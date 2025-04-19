from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
import os 
from.index import index_views

from App.controllers import (
    get_all_users,
    get_all_users_json,
    jwt_required
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    """
    Render the user page with all users.
    
    Returns:
        The rendered user.html template with all users.
    """
    users = get_all_users()
    return render_template('users.html', users=users)


@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    """
    Get a list of all users in json format.
    
    Returns:
        A json object containing a list of all users.
    """
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/static/users', methods=['GET'])
def static_user_page():
    """
    Return a static html page from the static directory.

    This endpoint is used to serve a static page for the user endpoint.
    The page is rendered on the client side.
    """
    return send_from_directory('static', 'static-user.html')

@user_views.route('/refcss', methods=['GET'])
def refresh_css():
    """
    Refresh the CSS by running the Tailwind CSS CLI command.

    This endpoint triggers a rebuild of the CSS file using Tailwind CSS.
    It executes a command to compile the CSS from input.css to output.css.

    Returns:
        None
    """
    # Execute the Tailwind CSS CLI command to regenerate the CSS
    os.system("npx @tailwindcss/cli -i App/static/Css/input.css -o App/static/Css/output.css")

    return redirect(url_for('index_views.index_page'))

