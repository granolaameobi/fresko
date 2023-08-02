from flask import Blueprint, render_template, session
from pos_app.models import get_stock, get_accessible_pages

view_stock_bp = Blueprint('view_stock', __name__)

@view_stock_bp.route('/view-stock')
def view_stock():
    current_stock = get_stock()
    # Check if the user_role is present in the session
    if 'user_role' in session:
        user_role = session['user_role']
    else:
        user_role = 'Signed out'  # Set a default value if user_role is not present

    accessible_pages = get_accessible_pages(user_role)
    return render_template('view-stock.html',
                           stock_data = current_stock,
                           accessible_pages = accessible_pages,
                           user_role = user_role)