from flask import Blueprint, render_template,request,redirect, url_for, session
from pos_app.models import get_orders, make_payment, get_orders_from_table

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


@payment_bp.route('/pay-total', methods=['POST'])
def pay_total(): 
    table_id = request.form.get('table_id')
    total_amount = request.form.get('total_cost')

    session['total_amount'] = total_amount
    session['table_id'] = table_id

    make_payment(table_id=table_id)

    # Redirect to the payment confirmation page
    return redirect(url_for('payment.payment_confirmation'))


@payment_bp.route('/payment-confirmation')
def payment_confirmation():
    # Retrieve the data from session
    total_amount = session.get('total_amount')
    table_id = session.get('table_id')

    # Clear the session data to avoid keeping unnecessary information
    session.pop('total_amount', None)
    session.pop('table_id', None)

    return render_template('payment-confirmation.html',
                           total_amount=total_amount,
                           table_id=table_id)