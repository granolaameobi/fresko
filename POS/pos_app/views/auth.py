from flask import Blueprint, render_template, session, request, redirect, url_for
from pos_app.models import get_accessible_pages, authenticate_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    # user_role = session.get('user_role')
    user_role = None

    if user_role is None:
        # Set user_role to None if not authenticated
        session['user_role'] = "Signed out"

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Call the authenticate_user function to get the user's role
        user_role = authenticate_user(username, password)

        if user_role:
            # Store the user's role in the session
            session['user_role'] = user_role
            accessible_pages = get_accessible_pages(user_role)
            return render_template('index.html', accessible_pages = accessible_pages)
        else:
            return render_template('login.html'
                                   , error='Invalid username or password'
                                   , user_role = session['user_role'])
    return render_template("login.html", user_role = session['user_role'])
    
    

@auth_bp.route('/log-out')
def logout():
    session.clear()
    user_role = "Signed out"
    return redirect(url_for('index'))