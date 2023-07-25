from flask import Blueprint, render_template , render_template, request, jsonify
from pos_app.models import get_stock

view_stock_bp = Blueprint('view_stock', __name__)

@view_stock_bp.route('/view-stock')
def view_stock():
    current_stock = get_stock()
    # print(current_stock)
    return render_template('view-stock.html',
                           stock_data = current_stock)