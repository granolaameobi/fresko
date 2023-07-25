from flask import Blueprint, render_template
from pos_app.models import get_orders

view_orders_bp = Blueprint('view_orders', __name__)

@view_orders_bp.route('/view-orders')
def view_orders():
    current_open_orders = get_orders('open')
    current_closed_orders = get_orders('closed')
    return render_template('view-orders.html',
                           open_orders_data = current_open_orders,
                           closed_orders_data = current_closed_orders)