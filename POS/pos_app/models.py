import psycopg2 
from collections import Counter
from datetime import datetime


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
            LEFT JOIN (
            SELECT DISTINCT table_id
            FROM "booking"
            WHERE start_time < '{start_time}'::timestamp + INTERVAL '{duration}'
            AND start_time + duration > '{start_time}'
            ) b ON t.table_id = b.table_id
            WHERE b.table_id IS NULL
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
        select_query = f"SELECT menu_item_id, menu_item_name, price, category \
                        FROM \"menu_item\" where category = '{course}';"
    else:
        select_query = f"SELECT menu_item_id, menu_item_name, price, category FROM \"menu_item\";"
    
    menu_items = SQL_query(select_query)

    # Extract item names/ids
    menu_ids, menu_names, prices, courses = zip(*menu_items)

    courses = list(courses)

    

    return list(menu_ids), list(menu_names), list(prices), courses


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
    query = """
        SELECT cs.ingredient_id, i.ingredient_name, cs.expiry_date, cs.quantity, i.unit
        FROM "current_stock" cs
        INNER JOIN "ingredient" i ON cs.ingredient_id = i.ingredient_id
    """
    stock_data = SQL_query(query)

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
    Fetches the current orders based on the given status.

    Parameters:
        status (str): The status of the orders to fetch (open or closed).

    Returns:
        list: A list of dictionaries containing order details with keys 'table_id', 'menu_item_name', 'price', and 'quantity'.
    '''

    query = f"SELECT table_id, menu_item_name, price, quantity, order_id \
                    FROM get_todays_orders() WHERE status = '{status}'"
            
    orders = SQL_query(query)

    return [
        {
            'table_id' : order[0],
            'menu_item_name' : order[1],
            'price' : order[2],
            'quantity': order[3],
            'order_id': order[4]
        }

        for order in orders
    ]


def get_order_total(order_id):
    """
    Get the total cost of an order from the database.

    Parameters:
        order_id (int): The unique identifier of the order.

    Returns:
        float: The total cost of the specified order as a float.

    This function queries the database to get the total cost of a specific order identified by the provided `order_id`.
    It uses the SQL function `get_order_total_cost` with the given order_id as an argument to calculate the total cost.
    The `SQL_query` function is responsible for executing the query and returning the result.

    Example:
        order_id = 123
        total_cost = get_order_total(order_id)
        print(f"The total cost of order {order_id} is £{total_cost}")
    """
    query = f'SElECT * from get_order_total_cost({order_id});'

    total = SQL_query(query)[0][0]

    total_float = float(total[1:])
    return total_float


def make_booking(table_ids, group_size, start_time, comment, duration = '2 hours'):
    """
    Make a booking for a group at one or more tables.

    Parameters:
        table_ids (list): List of integers representing the IDs of the tables to book.
        group_size (int): The size of the group for the booking.
        start_time (str): The start time of the booking in 'YYYY-MM-DD HH:MM:SS' format.
        comment (str): Any additional comment on the booking
        duration (str): The duration of the booking in 'HH:MM:SS' format.

    Returns:
        None

    Example:
        make_booking([1, 2, 3], 6, '2023-07-25 14:30:00', '2 gluten free people', '2 hours')
    """
    if comment:
        sql_booking = f"SELECT insert_booking(ARRAY{table_ids}, {group_size}, '{start_time}'::timestamp without time zone, '{duration}'::interval, '{comment}')"
    else:
        sql_booking = f"SELECT insert_booking(ARRAY{table_ids}, {group_size}, '{start_time}'::timestamp without time zone, '{duration}'::interval, 'None')"
    
    SQL_query(sql_booking, to_return_rows=False)


def get_table_order(table_id):
    '''
    Get all orders and the total cost for a specific table.

    This function retrieves all open orders with their details and the total cost
    for a specified table identified by the provided `table_id`. The function queries the
    database to find all open orders associated with the specified table, calculates the
    total cost for these orders, and returns the order details along with the total cost.

    Args:
        table_id (int): The ID of the table for which to retrieve orders and the total cost.

    Returns:
        tuple: A tuple containing two elements.
            - The first element is a list of dictionaries, each representing an order. Each
              dictionary contains the following keys:
                - 'order_id' (int): The ID of the order.
                - 'menu_item_name' (str): The name of the menu item.
                - 'price' (str): The price of the menu item as a string, e.g., '£15.99'.
                - 'quantity' (int): The quantity of the menu item ordered.
            - The second element is the total cost (float) for all orders on the table.

    '''

    query = f"SELECT order_id, menu_item_name, price, quantity FROM get_todays_orders() WHERE status = 'open' and table_id = {table_id}"
            
    items = SQL_query(query)

    _, _, prices, quantities = zip(*items)

    total_cost = sum([float(price[1:])*quantity for price, quantity in zip(prices, quantities)])

    order_details =  [
        {
            'order_id' : order[0],
            'menu_item_name' : order[1],
            'price' : order[2],
            'quantity': order[3],
        }

        for order in items
    ]

    return order_details, total_cost


    
def make_payment(table_id):
    '''
    Inserts a payment record into the "payment" table with the provided table_id.

    Parameters:
        amount (float): The payment amount.
        order_id (int): The order ID to associate the payment with.

    Returns:
        None
    '''
    orders_and_amounts = get_orders_from_table(table_id=table_id)
    payment_time = datetime.now()
    for order_id, amount in orders_and_amounts:
        print(f'Paying: {amount} on Order:{order_id}')
        sql_payment = f"""INSERT INTO payment (order_id, amount, payment_time)
                        VALUES ({order_id}, {amount}, '{payment_time}'); """
        SQL_query(sql_payment, to_return_rows=False)


def get_orders_from_table(table_id):
    """Retrieve order IDs and their respective totals for a given table.

    This function retrieves the order IDs and their corresponding totals for a specific table
    identified by the provided `table_id`. It queries the database to find the distinct order
    IDs associated with the specified table, then calculates the totals for each of those orders.

    Args:
        table_id (int): The ID of the table for which to retrieve orders and totals.

    Returns:
        tuple: A tuple containing two lists.
            - The first element is a list of order IDs (int) associated with the table.
            - The second element is a list of corresponding order totals (float).

    Example:
        >>> order_ids, totals = get_orders_from_table(3)
        >>> print(order_ids)
        [101, 102, 105]
        >>> print(totals)
        [24.99, 17.50, 38.75]
    """
    sql_order = f"SELECT distinct(order_id) from get_todays_orders() where table_id = {table_id};"
    order_ids_tuples = SQL_query(sql_order)
    order_ids = [order_id_tuple[0] for order_id_tuple in order_ids_tuples]
    totals = [get_order_total(order_id) for order_id in order_ids]


    return zip(order_ids, totals)

