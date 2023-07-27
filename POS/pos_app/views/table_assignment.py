from flask import Blueprint, render_template, request, redirect, url_for, flash
from pos_app.models import table_assigner, find_available_tables, make_booking

table_assignment_bp = Blueprint('table_assignment', __name__)

@table_assignment_bp.route('/table-assignment')
def table_assignment():
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

    print(assigned_tables)

    make_booking(assigned_tables, party_size, date_time, comment=comment)

    confirmation_details = {
        'date': date,
        'time': time,
        'party_size': party_size,
        'comment': comment,
        'assigned_tables' : assigned_tables
    }

    return render_template('table-confirmation.html', confirmation_details=confirmation_details)

