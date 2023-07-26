# Make sure to install the following libraries:
# pip install Flask
# pip install Flask-Login
# pip install Flask-SocketIO
# pip install Flask-Mail

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from flask_mail import Mail, Message
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Fresko2023@35.205.66.81/Fresko'  # Replaced with PostgreSQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'freskogreek@gmail.com'
app.config['MAIL_PASSWORD'] = 'Fresko2023'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'freskogreek@gmail.com'

db = SQLAlchemy(app)
mail = Mail(app)
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    availabilities = db.relationship('Availability', backref='user', lazy=True)
    shifts = db.relationship('Shift', backref='user', lazy=True)

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class ShiftSwapRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    your_shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)
    requested_shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=False)

    your_shift = db.relationship('Shift', foreign_keys=[your_shift_id], backref='shift_swap_requests_your_shift')
    requested_shift = db.relationship('Shift', foreign_keys=[requested_shift_id], backref='shift_swap_requests_requested_shift')

    def __repr__(self):
        return f"<ShiftSwapRequest id={self.id} Your Shift={self.your_shift} Requested Shift={self.requested_shift}>"

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#---------------------------------------------------------------------------------------------------------------------
# User authentication

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('manage_availability'))
        else:
            flash('Invalid username or password!', 'error')
    return render_template('login.html')

#---------------------------------------------------------------------------------------------------------------------
# User registration

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

#---------------------------------------------------------------------------------------------------------------------

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------------
# User availability management route

@app.route('/availability', methods=['GET', 'POST'])
@login_required
def manage_availability():
    if request.method == 'POST':
        # Get form data
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')

        # Create a new Availability instance
        new_availability = Availability(start_time=start_time, end_time=end_time, user=current_user)

        # Add the new availability to the database and commit the changes
        db.session.add(new_availability)
        db.session.commit()

        flash('Availability added successfully!', 'success')
        return redirect(url_for('manage_availability'))
    return render_template('availability.html')

# Delete availability route

@app.route('/delete_availability/<int:availability_id>', methods=['POST'])
@login_required
def delete_availability(availability_id):
    availability = Availability.query.get_or_404(availability_id)

    # Check if the availability belongs to the current user
    if availability.user != current_user:
        flash('You are not authorized to delete this availability.', 'error')
        return redirect(url_for('manage_availability'))

    # Delete the availability from the database
    db.session.delete(availability)
    db.session.commit()

    flash('Availability deleted successfully!', 'success')
    return redirect(url_for('manage_availability'))

#---------------------------------------------------------------------------------------------------------------------
# Shift management route

@app.route('/shifts', methods=['GET', 'POST'])
@login_required
def manage_shifts():
    if request.method == 'POST':
        # Get form data
        start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')

        # Create a new Shift instance
        new_shift = Shift(start_time=start_time, end_time=end_time, user=current_user)

        # Add the new shift to the database and commit the changes
        db.session.add(new_shift)
        db.session.commit()

        flash('Shift added successfully!', 'success')
        return redirect(url_for('manage_shifts'))

    return render_template('manage_shifts.html')

# Delete shift route

@app.route('/delete_shift/<int:shift_id>', methods=['POST'])
@login_required
def delete_shift(shift_id):
    shift = Shift.query.get_or_404(shift_id)

    # Check if the shift belongs to the current user
    if shift.user != current_user:
        flash('You are not authorized to delete this shift.', 'error')
        return redirect(url_for('manage_shifts'))

    # Delete the shift from the database
    db.session.delete(shift)
    db.session.commit()

    flash('Shift deleted successfully!', 'success')
    return redirect(url_for('manage_shifts'))

#---------------------------------------------------------------------------------------------------------------------
# Shift swap route

@app.route('/shift_swap', methods=['GET', 'POST'])
@login_required
def shift_swap():
    # Get available shifts for swapping (excluding the shifts of the current user)
    available_shifts = Shift.query.filter(Shift.user != current_user).all()

    if request.method == 'POST':
        # Get form data
        requested_shift_id = int(request.form['requested_shift'])

        # Find the requested shift in the available shifts
        requested_shift = next((shift for shift in available_shifts if shift.id == requested_shift_id), None)

        if requested_shift:
            # Create a new ShiftSwapRequest instance
            shift_swap_request = ShiftSwapRequest(your_shift=current_user.shifts[-1], requested_shift=requested_shift)
            socketio.emit('new_swap_request', {'request_id': shift_swap_request.id}, room=current_user.id)

            # Add the shift swap request to the database and commit the changes
            db.session.add(shift_swap_request)
            db.session.commit()

            flash('Shift swap request sent successfully!', 'success')
            return redirect(url_for('shift_swap'))
        else:
            flash('Invalid shift swap request.', 'error')

    # Get shift swap requests for the current user
    shift_swap_requests = ShiftSwapRequest.query.filter(ShiftSwapRequest.your_shift.has(user=current_user)).all()

    return render_template('shift_swap.html', available_shifts=available_shifts, shift_swap_requests=shift_swap_requests)

# Accept shift swap route

@app.route('/accept_swap/<int:request_id>', methods=['POST'])
@login_required
def accept_swap(request_id):
    shift_swap_request = ShiftSwapRequest.query.get_or_404(request_id)

    # Check if the shift swap request belongs to the current user
    if shift_swap_request.your_shift.user != current_user:
        flash('You are not authorized to accept this shift swap request.', 'error')
        return redirect(url_for('shift_swap'))

    # Swap the shifts
    your_shift = shift_swap_request.your_shift
    requested_shift = shift_swap_request.requested_shift

    your_shift.start_time, requested_shift.start_time = requested_shift.start_time, your_shift.start_time
    your_shift.end_time, requested_shift.end_time = requested_shift.end_time, your_shift.end_time

    db.session.commit()

    flash('Shift swap request accepted. Your shift has been swapped!', 'success')
    return redirect(url_for('shift_swap'))

#---------------------------------------------------------------------------------------------------------------------
# Email notifications using Flask-Mail

def send_email_notification(subject, body, recipient):
    msg = Message(subject=subject, body=body, recipients=[recipient])
    mail.send(msg)

# Notifications route

@app.route('/notifications', methods=['GET', 'POST'])
@login_required
def notifications():
    if request.method == 'POST':
        # Get form data
        subject = request.form['subject']
        body = request.form['body']
        recipient = request.form['recipient']

        # Send email notification
        send_email_notification(subject, body, recipient)

        flash('Email notification sent successfully!', 'success')

    return render_template('notifications.html')

@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)