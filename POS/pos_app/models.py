import psycopg2 
from collections import Counter
from flask import session


# Connect to the PostgreSQL database
def connect_to_database():
    '''
    Connects to postgreSQL database
    
    If unsuccessful, resturns the error recieved
    '''
    try:
        connection = psycopg2.connect(
            host="127.0.0.1",
            database="Restaurant",
            user="postgres", #Remember to change these details
            password="PostGres"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Database Connection Error", str(error))
        return None
    

def SQL_query(select_query, to_return_rows=True):
    """
    Executes the given SQL query and returns the result if specified.

    Inputs:
    - select_query (str): The SQL query to execute.
    - to_return_rows (bool): Indicates whether to fetch and return rows (default: True).

    Returns:
    - rows (list): The fetched rows if `to_return_rows` is True, else None.
    """
    connection = connect_to_database()
    cursor = connection.cursor()

    cursor.execute(select_query)

    if to_return_rows:
        # Fetch all the rows returned by the query
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    else:
        cursor.close()
        connection.commit()  # Commit the transaction
        connection.close()

def find_available_tables(start_time, duration = '2 hours'):
    '''
    Finds the available tables based on the given start time and duration.

    Inputs:
    - start_time: A string representing the start time in the format 'YYYY-MM-DD HH:MM:SS'.
    - duration: An string of the interval in valid format for SQL e.g. '2 hours'

    Returns:
    - tables: A list of tuples containing the available table IDs and their capacities.
              Each tuple has the format (table_id, capacity).
    '''

    # Connect to the PostgreSQL database
    tables_query = f""" 
            SELECT t.table_id, t.capacity 
            FROM "table_number" t 
            LEFT JOIN "booking" b ON t.table_id = b.table_id 
            WHERE (b.start_time IS NULL OR b.start_time + b.duration <= '{start_time}' 
                OR '{start_time}' >= b.start_time + interval '{duration}')  
        """

    tables = SQL_query(tables_query)

    return tables



def table_assigner(available_tables, party_size, table_combination=[]):
    '''
    Assigns tables for a given party size from the list of available tables.

    Inputs:
    - available_tables: A list of tuples containing the available table IDs and their capacities.
                        Each tuple has the format (table_id, capacity).
    - party_size: An integer representing the size of the party.
    - table_combination: (optional) A list containing the previously assigned table IDs.
                         This parameter is used for recursive calls.

    Returns:
    - table_combination: A list of table IDs that can accommodate the party size.
                         If no suitable combination is found, it returns a message string.
    '''

    # If the party size is non-positive, return the assigned tables
    if party_size <= 0:
        return table_combination

    # Sort tables from smallest to largest
    available_tables.sort(key=lambda x: x[1], reverse=False)

    # If party size is smaller than the capacity of the smallest table,
    # assign the smallest table
    smallest_table = available_tables[0]
    if party_size < smallest_table[1]:
        table_combination.append(smallest_table[0])
        return table_combination

    # Try to assign the party to a table of the exact size
    for table_id, capacity in available_tables:
        if capacity == party_size:
            table_combination.append(table_id)
            return table_combination

    # Find the smallest table that can accommodate the party size or is slightly larger
    candidate_table_capacity = party_size + 2
    candidate_id = None
    for table_id, capacity in available_tables:
        if capacity >= party_size and capacity <= candidate_table_capacity:
            candidate_table_capacity = capacity
            candidate_id = table_id

    # If a suitable table is found, assign it
    if candidate_id:
        table_combination.append(candidate_id)
        return table_combination

    # Extract table IDs and capacities to make the next part easier
    ids, capacities = zip(*available_tables)

    # Check if the total capacity of available tables is insufficient for the party size
    if sum(list(capacities)) < party_size:
        print('No available tables for that size')
        return 'No available tables for that size'

    # Assign the party to the largest available table
    available_tables.sort(key=lambda x: x[1], reverse=True)
    biggest_table = available_tables[0]
    table_combination.append(biggest_table[0])

    # Remove the assigned table from the available tables and reduce the party size
    available_tables.remove(biggest_table)
    party_size -= biggest_table[1]

    # Restart the table assignment process recursively
    return table_assigner(available_tables, party_size, table_combination)



    

def get_menu_items(course=None):
    '''
    Retrieves the menu items from the database.

    Args:
    - course: (optional) Course name to filter menu items. If None, retrieves all menu items.

    Returns:
    - menu_names: A list of menu item names.
    - menu_ids: A list of menu item IDs.
    - prices: A list of menu item prices.
    - courses: A list of menu item courses.
    '''
    if course:
        select_query = f"SELECT menu_item_id, menu_item_name, price, catgeory \
                        FROM \"menu_item\" where catgeory = '{course}';"
    else:
        select_query = f"SELECT menu_item_id, menu_item_name, price, catgeory FROM \"menu_item\";"
    
    menu_items = SQL_query(select_query)

    # Extract item names/ids
    menu_ids, menu_names, prices, courses = zip(*menu_items)

    return list(menu_ids), list(menu_names), list(prices), list(courses)


def get_tables_numbers():
        '''
        Retrieves the table numbers from the database.

        Returns:
        - table_numbers: A list of table numbers.
        '''
        try:
            # Execute the SQL query to select table numbers
            select_query = "SELECT table_id FROM \"table_number\";"

            # Fetch all the rows returned by the query
            table_numbers = SQL_query(select_query)

            # Extract as list of strings
            table_numbers = ['Table ' + str(number[0]) for number in table_numbers]
            return table_numbers
        except Exception as e:
            print("Error", str(e))



def place_order(order_ids, table_id):
    """
    Place an order by calling a PostgreSQL function with the provided order IDs and quantities.

    Parameters:
        order_ids (list): A list of unique item IDs representing the items to be ordered.
        table_id (int): The ID of the table where the order is placed.

    Returns:
        None: This function doesn't return any value directly, but it places an order in the PostgreSQL database.
    """
    # Find IDs and quantities in orders
    ids = []
    quantities = []
    for item_id, quantity in Counter(order_ids).items():
        ids.append(int(item_id))
        quantities.append(int(quantity))

    # Execute query to call function in PostgreSQL
    select_query = f"SELECT create_new_order(ARRAY{ids}, \
                    ARRAY{quantities}, {table_id});"
    #Execute the SQL query
    SQL_query(select_query, to_return_rows= False)


def authenticate_user(username, password):
    # Connect to the database (replace these with your actual database connection details)
    # connection = connect_to_database()
    # cursor = connection.cursor()

    # Hash the password (you should use a strong password hashing library like bcrypt)
    # hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username == 'a' and password == 'p':
        print('You are an admin')
        return 'admin' #For now just change this to what I want
    else:
        print('No authentication for you!')
        return None
    #Not in DB yet -> add this when back
    # # Execute the SQL query to retrieve the user's role
    # select_query = f"SELECT role FROM users WHERE username = {username} AND password = {password};"
    
    # # Fetch the result
    # result = SQL_query(select_query=select_query)

    # Return the user's role or None if authentication fails
    # if result:
    #     return result[0]
    # else:
    #     return None


def get_accessible_pages(user_role):
    """
    Get a dictionary of accessible pages based on the user's role.

    Parameters:
        user_role (str): The role of the user. Can be 'admin', 'manager', 'staff', or other roles.

    Returns:
        dict: A dictionary representing the accessible pages for the given user role.

    Explanation:
    """
    accessible_pages = {
        'new_order': user_role in ['admin', 'manager', 'staff'],
        'view_orders': user_role in ['admin', 'manager', 'staff'],
        'payment': user_role in ['admin', 'manager', 'staff'],
        'view_stock': user_role in ['admin', 'manager'],
        'table_assignment': user_role in ['admin', 'manager', 'staff'],
        'sign_out': user_role != None
    }
    return accessible_pages

def get_stock():
    """
    Fetches the current stock data.
    """
    # try:
        # query = """
        #     SELECT cs.ingredient_id, i.ingredient_name, cs.expiry_date, cs.quantity, cs.units
        #     FROM "Current_stock" cs
        #     INNER JOIN "Ingredient" i ON cs.ingredient_id = i.ingredient_id
        # """
        # stock_data = SQL_query(query)

    stock_data = [(1,'Ing 1', '22/07/2022', 4, 'kg')]
    return [
            {
                'ingredient_id': stock[0],
                'ingredient_name': stock[1],
                'expiry_date': stock[2],
                'quantity': stock[3],
                'units': stock[4]
            }
            for stock in stock_data
        ]



def get_orders(status):
    '''
    Fetches the current orders
    '''

    query = f"SELECT table_id, menu_item_name, price, quantity \
                    FROM get_todays_orders() WHERE status = '{status}'"
            
    orders = SQL_query(query)

    return [
        {
            'table_id' : order[0],
            'menu_item_name' : order[1],
            'price' : order[2],
            'quantity': order[3]
        }

        for order in orders
    ]