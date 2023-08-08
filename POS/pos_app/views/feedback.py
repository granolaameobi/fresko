from flask import Blueprint, render_template, session, request
from pos_app.models import  get_accessible_pages, submit_feedback_to_db

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback')
def feedback():
    # Check if the user_role is present in the session
    if 'user_role' in session:
        user_role = session['user_role']
    else:
        user_role = 'Signed out'  # Set a default value if user_role is not present

    accessible_pages = get_accessible_pages(user_role)
    return render_template('feedback.html',
                           accessible_pages = accessible_pages,
                           current_page = 'feedback')

@feedback_bp.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    rating = request.form.get('rating') 

    submit_feedback_to_db(name, rating, email, message)

    # Check if the user_role is present in the session
    if 'user_role' in session:
        user_role = session['user_role']
    else:
        user_role = 'Signed out'  # Set a default value if user_role is not present

    accessible_pages = get_accessible_pages(user_role)

    return render_template('feedback-confirmation.html',
                           name = name,
                           rating = rating,
                           email = email,
                           message = message,
                           accessible_pages = accessible_pages,
                           user_role = user_role,
                           current_page = 'feedback')