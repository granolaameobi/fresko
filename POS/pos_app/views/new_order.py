from flask import Blueprint, render_template, request, jsonify
from pos_app.models import get_menu_items, place_order, get_tables_numbers

new_order_bp = Blueprint('new_order', __name__)

@new_order_bp.route('/new-order')
def new_order():
    _,_,_, menu_courses = get_menu_items()
    course_names = list(set(menu_courses))

    menu_data = dict()

    print(menu_courses)

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
    
    table_numbers = get_tables_numbers()

    return render_template('new-order.html',
                           menu_data=menu_data,
                           table_numbers = table_numbers)

@new_order_bp.route('/confirm_order', methods=['POST'])
def confirm_order():
    order_data = request.get_json()
    
    # Extract item_ids and table_number from the nested dictionary
    item_ids = order_data.get('itemIds', [])
    table_name = order_data.get('tableNumber')


    table_number = int(table_name.split(' ')[-1])
    # Here, you can process the confirmed order as needed

    place_order(item_ids, table_number)
    # print(f"Confirmed Order:{item_ids} on Table {table_number}")
    return jsonify({"message": "Order confirmed successfully!"})