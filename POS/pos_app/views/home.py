from flask import Blueprint, render_template, session, request
from pos_app.models import get_accessible_pages

home_bp = Blueprint('home', __name__)

@home_bp.route('/home', methods=['POST', 'GET'])
def home():
        user_role = session['user_role']
        accessible_pages = get_accessible_pages(user_role)
        return render_template('index.html', accessible_pages = accessible_pages)