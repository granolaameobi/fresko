from flask import Blueprint, render_template, session
from pos_app.models import get_orders, get_accessible_pages

view_orders_bp = Blueprint('view_orders', __name__)

@view_orders_bp.route('/view-orders')
def view_orders():
    current_open_orders = get_orders('open')
    current_closed_orders = get_orders('closed')

    # Check if the user_role is present in the session
    if 'user_role' in session:
        user_role = session['user_role']
    else:
        user_role = 'Signed out'  # Set a default value if user_role is not present

    accessible_pages = get_accessible_pages(user_role)
    return render_template('view-orders.html',
                           open_orders_data = current_open_orders,
                           closed_orders_data = current_closed_orders,
                           accessible_pages = accessible_pages,
                           user_role = user_role,
                           current_page = 'view-orders')