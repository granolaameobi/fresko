from flask import Blueprint, render_template, request, session
from pos_app.models import table_assigner, find_available_tables, make_booking, get_accessible_pages
from datetime import datetime

table_assignment_bp = Blueprint('table_assignment', __name__)

@table_assignment_bp.route('/table-assignment')
def table_assignment():

    # Check if the user_role is present in the session
    if 'user_role' in session:
        user_role = session['user_role']
    else:
        user_role = 'Signed out'  # Set a default value if user_role is not present

    accessible_pages = get_accessible_pages(user_role)
    return render_template('table-assignment.html',
                           accessible_pages = accessible_pages,
                           user_role = user_role)


@table_assignment_bp.route('/reservation', methods=['POST'])
def handle_reservation():
    date = request.form.get('date')
    time = request.form.get('time')
    party_size = int(request.form.get('party_size'))
    comment = request.form.get('comment')

    #Combine date and time to enter to SQL
    date_time = date +' ' + time

    #If date or time not selected, take current time
    if len(date_time) < 16:
        date_time = str(datetime.now())[:-7]
        date = date_time.split(' ')[0]
        time = date_time.split(' ')[1]

    #Find avilable tables for th group size
    available_tables = find_available_tables(start_time=date_time)
    assigned_tables = table_assigner(available_tables, party_size)

    #Enter a booking on those tables
    make_booking(assigned_tables, party_size, date_time, comment=comment)

    #Send the confirmation details
    confirmation_details = {
        'date': date,
        'time': time,
        'party_size': party_size,
        'comment': comment,
        'assigned_tables' : assigned_tables
    }
    return render_template('table-confirmation.html', confirmation_details=confirmation_details)

