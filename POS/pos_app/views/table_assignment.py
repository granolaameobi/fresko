from flask import Blueprint, render_template, request
from pos_app.models import table_assigner, find_available_tables

table_assignment_bp = Blueprint('table_assignment', __name__)

@table_assignment_bp.route('/table-assignment')
def view_stock():
    return render_template('table-assignment.html')


@table_assignment_bp.route('/reservation', methods=['POST'])
def handle_reservation():
    date = request.form.get('date')
    time = request.form.get('time')
    party_size = int(request.form.get('party_size'))
    comment = request.form.get('comment')

    date_time = date +' ' + time
    available_tables = find_available_tables(date_time)
    assigned_tables = table_assigner(available_tables, party_size)

    return f'Assigned on {assigned_tables}, with comment {comment}'