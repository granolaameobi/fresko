from flask import Flask, render_template, session
from pos_app.views.new_order import new_order_bp
from pos_app.views.auth import auth_bp
from pos_app.views.home import home_bp
from pos_app.views.view_stock import view_stock_bp
from pos_app.views.view_orders import view_orders_bp
from pos_app.views.table_assignment import table_assignment_bp
from pos_app.views.payment import payment_bp
from pos_app.views.feedback import feedback_bp
from pos_app.models import get_accessible_pages

# Set up the flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Register the Blueprints
app.register_blueprint(new_order_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(view_stock_bp)
app.register_blueprint(view_orders_bp)
app.register_blueprint(table_assignment_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(feedback_bp)


# Home route to render index.html
@app.route('/')
def index():
    #Check if user signed in
    if 'user_role' in session:
        user_role = session['user_role']
        accessible_pages = get_accessible_pages(user_role)
    else:
        user_role = 'Signed out' 
        accessible_pages = get_accessible_pages(None)
    return render_template('index.html',
                        accessible_pages = accessible_pages,
                        user_role = user_role)

