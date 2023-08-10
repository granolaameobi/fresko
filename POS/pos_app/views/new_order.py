from flask import Blueprint, render_template, request, jsonify, session
from pos_app.models import get_menu_items, place_order, get_tables_numbers, get_accessible_pages

new_order_bp = Blueprint('new_order', __name__)

@new_order_bp.route('/new-order')
def new_order():
    _,_,_, menu_courses = get_menu_items()
    course_names = list(set(menu_courses))

    menu_data = dict()

    for course in course_names:
        ids,names,prices,_ = get_menu_items(course=course)

        if course in ['wine', 'drink', 'beer', 'fresko cocktail', 'mocktail', 'classic cocktail', 'cider']:
            course = 'drink'
        if course == 'add-on':
            course = 'add_on'
        if course == 'hot meze':
            course = 'hot_meze'
        if course == 'cold meze':
            course = 'cold_meze'


        menu_data[course] = zip(ids, names, prices)

        # Check if the user_role is present in the session
    if 'user_role' in session:
        user_role = session['user_role']
    else:
        user_role = 'Signed out'  # Set a default value if user_role is not present

    accessible_pages = get_accessible_pages(user_role)
    
    table_numbers = get_tables_numbers()

    return render_template('new-order.html',
                           menu_data=menu_data,
                           table_numbers = table_numbers,
                           accessible_pages = accessible_pages,
                           user_role = user_role,
                           current_page = 'new-order')

@new_order_bp.route('/confirm_order', methods=['POST'])
def confirm_order():
    order_data = request.get_json()
    
    # Extract item_ids, table_number, and comments from the nested dictionary
    item_data = order_data.get('items', [])
    table_name = order_data.get('tableNumber')

    # Extract item details including comments
    item_ids = [item['id'] for item in item_data]
    comments = [item['comment'] for item in item_data]


    table_number = int(table_name.split(' ')[-1])
    # Here, you can process the confirmed order as needed

    place_order(item_ids, table_number, comments)
    return jsonify({"message": "Order confirmed successfully!"})