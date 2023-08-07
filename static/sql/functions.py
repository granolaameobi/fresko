import psycopg2 


# Connect to the PostgreSQL database
def connect_to_database(host, database, user, password):
    '''
    Connects to postgreSQL database
    
    If unsuccessful, resturns the error recieved
    '''
    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user, #Remember to change these details
            password=password
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Database Connection Error", str(error))
        return None

def find_available_tables(start_time, duration, host, database, user, password):
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
    connection = connect_to_database(host=host,database=database,user=user,
                                     password=password)
    cursor = connection.cursor()

    
    try:
        # Execute the SQL query to find available tables
        cursor.execute(f""" 
            SELECT t.table_id, t.capacity
            FROM "table_number" t
            LEFT JOIN (
            SELECT DISTINCT table_id
            FROM "booking"
            WHERE start_time < '{start_time}'::timestamp + INTERVAL '{duration}'
            AND start_time + duration > '{start_time}'
            ) b ON t.table_id = b.table_id
            WHERE b.table_id IS NULL 
        """)

        # Fetch all the rows returned by the query
        rows = cursor.fetchall()

        # Extract table IDs and capacities from the rows
        tables = rows
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 


    # Close the database connection
    cursor.close()
    connection.close()

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

    party_size=int(party_size)

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


def SQL_query(select_query, host, database, user, password, to_return_rows=True):
    """
    Executes the given SQL query and returns the result if specified.

    Inputs:
    - select_query (str): The SQL query to execute.
    - to_return_rows (bool): Indicates whether to fetch and return rows (default: True).

    Returns:
    - rows (list): The fetched rows if `to_return_rows` is True, else None.
    """
    connection = connect_to_database(host, database, user, password)
    cursor = connection.cursor()

    cursor.execute(select_query)

    if to_return_rows:
        # Fetch all the rows returned by the query
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows
    else:
        # Execute the query without returning rows
        cursor.execute(select_query)
        cursor.close()
        connection.commit()  # Commit the transaction
        connection.close()
