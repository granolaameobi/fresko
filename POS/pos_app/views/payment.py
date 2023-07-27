from flask import Blueprint, render_template
from pos_app.models import get_orders

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment')
def payment():
    current_open_orders = get_orders('open')
    table_numbers = set()
    for order in current_open_orders:
        table_numbers.add(order['table_id'])

    table_numbers = list(table_numbers)
    table_numbers.sort()

    # print(table_numbers)
    return render_template('payment.html',
                           open_orders = current_open_orders,
                           table_numbers = table_numbers)

