from flask import Blueprint, render_template, session, redirect, url_for
from pos_app.models import get_accessible_pages, SQL_query

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['POST', 'GET'])
def home():
    # Check if the user_role is present in the session
    if 'user_role' in session:
        user_role = session['user_role']
    else:
        user_role = 'Signed out'  # Set a default value if user_role is not present

    accessible_pages = get_accessible_pages(user_role)

    return render_template('index.html', user_role=user_role, accessible_pages=accessible_pages)



@home_bp.route('/dummy-orders', methods=['POST', 'GET'])
def dummy_orders():
    # Call the SQL_query function to create dummy orders
    SQL_query('SELECT * FROM create_dummy_orders()', to_return_rows=False)

    # Redirect to the home page
    return redirect(url_for('home.home'))