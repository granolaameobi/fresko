import tkinter as tk
from tkinter import ttk, Scrollbar, messagebox
import psycopg2
from collections import Counter
from POS_functions import table_assigner, find_available_tables, connect_to_database, SQL_query
from datetime import datetime


class WelcomeWindow(tk.Tk):
    '''
    Represents the welcome window of the POS System.

    Inherits from tk.Tk class

    Methods:
    - __init__: Initializes the WelcomeWindow object.
    - open_sign_in: Opens the sign-in menu.
    '''

    def __init__(self):
        '''
        Initializes the WelcomeWindow object.

        Sets the window title, background color, and maximizes the window.
        Creates labels and buttons for the welcome message, sign-in, and exit.
        '''
        super().__init__()
        self.title("POS System")
        self.configure(background='#C0D5B2')
        self.state("zoomed")

        label_title = tk.Label(self, text="Welcome to the POS System!")
        label_title.pack(padx=10, pady=10)

        button_start = tk.Button(self, text="Sign In", command=self.open_sign_in)
        button_start.pack(padx=10, pady=5)

        button_exit = tk.Button(self, text="Exit", command=self.destroy)
        button_exit.pack(padx=10, pady=5)

    def open_sign_in(self):
        '''
        Opens the sign-in menu.

        Hides the current window and opens the sign-in menu window.
        '''
        self.withdraw()
        SignInMenu(self)  # change this during testing
        # NewOrderSubmenu(self)


class SignInMenu(tk.Toplevel):
    '''
    Represents the sign-in menu of the POS System.

    Inherits from tk.Toplevel class.

    Methods:
    - __init__: Initializes the SignInMenu object.
    - check_credentials: Validates the user credentials.
    - close_submenu: Closes the sign-in menu and shows the main menu.
    '''

    def __init__(self, parent):
        '''
        Initializes the SignInMenu object.

        Sets the window title, background color, and maximizes the window.
        Creates labels and entry fields for the user ID and password.
        Creates buttons for entering the credentials and going back.
        '''
        super().__init__(parent)
        self.title("POS System")
        self.configure(background='#C0D5B2')
        self.state("zoomed")

        label_title = tk.Label(self, text="Please sign in")
        label_title.pack(padx=10, pady=10)

        # Username field
        label_user_id = tk.Label(self, text="User ID:")
        label_user_id.pack(padx=10, pady=5)
        self.entry_user_id = tk.Entry(self)
        self.entry_user_id.pack(padx=10, pady=5)

        # Password field
        label_password = tk.Label(self, text="Password:")
        label_password.pack(padx=10, pady=5)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(padx=10, pady=5)

        # Enter button
        button_enter = tk.Button(self, text="Enter", command=self.check_credentials)
        button_enter.pack(padx=10, pady=5)

        # Back button
        button_back = tk.Button(self, text="Back", command=self.close_submenu)
        button_back.pack(padx=10, pady=5)

    def check_credentials(self):
        '''
        Validates the user credentials.

        Retrieves the user ID and password entered by the user.
        Clears the entry fields.
        If the credentials are valid, hides the sign-in menu and shows the main menu.
        Otherwise, displays an error message.
        '''
        user_id = self.entry_user_id.get()
        password = self.entry_password.get()

        # Clear the entries
        self.entry_user_id.delete(0, 'end')
        self.entry_password.delete(0, 'end')

        if user_id == 'User' and password == 'pass':
            self.withdraw()
            MainMenu(self)
        else:
            messagebox.showerror("Credential Error", "Username or Password was incorrect\n\nTry again")

    def close_submenu(self):
        '''
        Closes the sign-in menu and shows the main menu.
        '''
        self.destroy()  # Destroy the submenu
        self.master.deiconify()  # Show the main menu


class MainMenu(tk.Toplevel):
    '''
    Represents the main menu of the POS System.

    Inherits from tk.Toplevel class.

    Methods:
    - __init__: Initializes the MainMenu object.
    - open_view_order_submenu: Opens the view orders submenu.
    - open_new_order_submenu: Opens the new order submenu.
    - open_new_table_submenu: Opens the table assignment submenu.
    - open_stock_submenu: Opens the stock counts submenu.
    - open_payment_submenu: Opens the payment submenu.
    - close_submenu: Closes the main menu and shows the previous menu.
    '''

    def __init__(self, parent):
        '''
        Initializes the MainMenu object.

        Sets the window title, background color, and maximizes the window.
        Creates labels and buttons for the main menu options.
        '''
        super().__init__(parent)
        self.title("POS System")
        self.configure(background='#C0D5B2')
        self.state("zoomed")

        label_title = tk.Label(self, text="Main Menu")
        label_title.pack(padx=10, pady=10)
        label_menu = tk.Label(self, text="Select an option:")
        label_menu.pack(padx=10, pady=10)

        # View Orders button
        button_orders = tk.Button(self, text="View Orders", command=self.open_view_order_submenu)
        button_orders.pack(padx=10, pady=5)

        # New Order button
        button_food = tk.Button(self, text="New Order", command=self.open_new_order_submenu)
        button_food.pack(padx=10, pady=5)

        # New table button
        button_tables = tk.Button(self, text="Table Assignment", command=self.open_new_table_submenu)
        button_tables.pack(padx=10, pady=5)

        # Payment button
        button_payment = tk.Button(self, text="Payment", command=self.open_payment_submenu)
        button_payment.pack(padx=10, pady=5)

        # Stock Counts button
        button_stock = tk.Button(self, text="Stock Counts", command=self.open_stock_submenu)
        button_stock.pack(padx=10, pady=5)

        # Exit button
        button_exit = tk.Button(self, text="Exit", command=self.close_submenu)
        button_exit.pack(padx=10, pady=5)

    def open_view_order_submenu(self):
        '''
        Opens the view orders submenu.

        Hides the current menu and opens the view orders submenu.
        '''
        self.withdraw()  # Hide the main menu
        ViewOrderSubmenu(self)

    def open_new_order_submenu(self):
        '''
        Opens the new order submenu.

        Hides the current menu and opens the new order submenu.
        '''
        self.withdraw()  # Hide the current menu
        NewOrderSubmenu(self)

    def open_new_table_submenu(self):
        '''
        Opens the table assingment submenu.

        Hides the current menu and opens the table assingment submenu.
        '''
        self.withdraw()  # Hide the current menu
        TableAssignmentSubmenu(self)

    def open_stock_submenu(self):
        '''
        Opens the stock counts submenu.

        Hides the current menu and opens the stock counts submenu.
        '''
        self.withdraw()  # Hide the current menu
        StockSubmenu(self)

    def open_payment_submenu(self):
        '''
        Opens the payment submenu.

        Hides the current menu and opens the payment submenu.
        '''
        self.withdraw()  # Hide the current menu
        PaymentSubmenu(self)

    def close_submenu(self):
        '''
        Closes the main menu and shows the previous menu.
        '''
        self.destroy()  # Destroy the submenu
        self.master.deiconify()  # Show the main menu



class NewOrderSubmenu(tk.Toplevel):
    '''
    Represents the new order submenu of the POS System.

    Inherits from tk.Toplevel class.

    Methods:
    - __init__: Initializes the NewOrderSubmenu object.
    - get_menu_items: Retrieves the menu items from the database.
    - get_tables_numbers: Retrieves the table numbers from the database.
    - create_button_grid: Creates the button grid for menu items.
    - display_menu_items: Displays the menu items for a given course.
    - add_to_order: Adds an item to the order.
    - show_order: Updates the treeview with the current order.
    - clear_order: Clears the current order.
    - confirm_order: Confirms the order and adds it to the database.
    - close_submenu: Closes the new order submenu and shows the previous menu.
    '''

    def __init__(self, parent):
        '''
        Initializes the NewOrderSubmenu object.

        Sets the window title, background color, and maximizes the window.
        Retrieves menu items and table numbers from the database.
        Creates labels, buttons, dropdown menu, and treeview for the new order submenu.
        '''
        super().__init__(parent)
        self.title("POS System")
        self.configure(background='#C0D5B2')
        self.state("zoomed")

        # New order
        self.default_option_table = "Select a table number"  # Default option for table dropdown menu
        self.selected_table = tk.StringVar(self)  # The selected table will be shown as a string
        table_list = self.get_tables_numbers()  # List of tables
        self.clear_order()

        # Menu Items -> Get from PostgreSQL database
        (
            self.overall_menu_ids,
            self.overall_menu_names,
            self.overall_prices,
            self.overall_courses
        ) = self.get_menu_items()
        self.course_names = list(set(self.overall_courses))

        # Set up frame for food options
        label_menu_options = tk.Label(self, text="Menu Options", font=('arial', 12, 'bold'))
        label_menu_options.pack(padx=10, pady=10)

        # Create a tabbed layout
        tab_control = ttk.Notebook(self)

        for course_name in self.course_names:
            tab = ttk.Frame(tab_control)
            tab_control.add(tab, text=course_name.capitalize() + "s")
            self.create_button_grid(course_name, tab)

        tab_control.pack()

        # Create Dropdown menu for table selection
        drop = tk.OptionMenu(self, self.selected_table, *table_list)
        drop.pack(pady=40)

        button_confirm_order = tk.Button(self, text="Confirm order", command=self.confirm_order)
        button_confirm_order.pack(padx=10, pady=5)

        # Back button
        button_back = tk.Button(self, text="Back to Main Menu", command=self.close_submenu)
        button_back.pack(padx=10, pady=5)

        # Create the treeview to display the order
        self.treeview = ttk.Treeview(self, columns=("Item Name", "Type", "Price"))
        self.treeview.heading("#0", text="Item Name")
        self.treeview.heading("#1", text="Type")
        self.treeview.heading("#2", text="Price")
        self.treeview.pack(padx=10, pady=10)

        # Show the order in the treeview
        self.show_order()

        button_clear_order = tk.Button(self, text="Clear order", command=self.clear_order)
        button_clear_order.pack(padx=10, pady=5)

    def get_menu_items(self, course=None):
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

        try:
            # Execute the SQL query to select menu item IDs and names
            if course:
                select_query = f"SELECT menu_item_id, menu_item_name, price, course \
                                FROM \"Menu_item\" where course = '{course}';"
            else:
                select_query = f"SELECT menu_item_id, menu_item_name, price, course FROM \"Menu_item\";"
            
            menu_items = SQL_query(select_query)

            # Extract item names/ids
            menu_ids, menu_names, prices, courses = zip(*menu_items)

            return list(menu_ids), list(menu_names), list(prices), list(courses)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def get_tables_numbers(self):
        '''
        Retrieves the table numbers from the database.

        Returns:
        - table_numbers: A list of table numbers.
        '''
        try:
            # Execute the SQL query to select table numbers
            select_query = "SELECT table_id FROM \"Table_number\";"

            # Fetch all the rows returned by the query
            table_numbers = SQL_query(select_query)

            # Extract as list of strings
            table_numbers = ['Table ' + str(number[0]) for number in table_numbers]
            return table_numbers
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def create_button_grid(self, course, tab):
        '''
        Creates the button grid for menu items in a specific course.

        Args:
        - course: The course name for which the buttons are created.
        - tab: The tab where the buttons are placed.
        '''
        frame_buttons = tk.Frame(tab, background='#C0D5B2')
        frame_buttons.pack(padx=10, pady=5)

        buttons = []
        ids, names, prices, courses = self.get_menu_items(course)
        for i, item in enumerate(names):
            button = tk.Button(
                frame_buttons,
                text=item,
                command=lambda i=i: self.add_to_order(names[i], ids[i], prices[i], courses[i])
            )
            button.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            buttons.append(button)

    def add_to_order(self, name, item_id, price, course):
        '''
        Adds an item to the order.

        Args:
        - name: The name of the item.
        - item_id: The ID of the item.
        - price: The price of the item.
        - course: The course of the item.
        '''
        self.order_names.append(name)
        self.order_ids.append(item_id)
        self.order_prices.append(price)
        self.order_courses.append(course)
        self.show_order()  # Update the treeview with the new item

    def show_order(self):
        '''
        Updates the treeview with the current order.
        '''
        self.treeview.delete(*self.treeview.get_children())

        # Insert the items from the order into the treeview
        for name, course, price in zip(self.order_names, self.order_courses, self.order_prices):
            self.treeview.insert("", tk.END, text=name, values=(course.capitalize(), price))

        total_price = sum([float(price[1:]) for price in self.order_prices])
        self.treeview.insert("", tk.END, text='TOTAL', values=(38 * '-', f'£{total_price:.2f}'))

    def clear_order(self):
        '''
        Clears the current order.
        '''
        self.order_names = []
        self.order_ids = []
        self.order_prices = []
        self.order_courses = []
        self.selected_table.set(self.default_option_table)
        try:
            self.show_order()
        except:
            pass

    def confirm_order(self):
        '''
        Confirms the order and adds it to the database.
        '''
        if self.selected_table.get() == self.default_option_table:
            messagebox.showerror("No Table Selected", "No Table\n\nPlease select a table")
            return
        else:
            # Convert to just ID of table
            selected_table_id = self.selected_table.get().split(' ')[-1]

        # Check there are items to be added
        if len(self.order_ids) == 0:
            messagebox.showerror("Empty Order", "Empty order\n\nPlease add some items")
            return

        try:
            # Find IDs and quantities in orders
            self.ids = []
            self.quantities = []
            for item_id, quantity in Counter(self.order_ids).items():
                self.ids.append(int(item_id))
                self.quantities.append(int(quantity))

            # Execute query to call function in PostgreSQL
            select_query = f"SELECT create_new_order(ARRAY{self.ids}, \
                            ARRAY{self.quantities}, {selected_table_id});"
            
            #Execute the SQL query
            SQL_query(select_query, to_return_rows= False)

            messagebox.showinfo("Order confirmed", f"Order has been placed on: Table {selected_table_id}.")
            # Empty the order
            self.clear_order()

        # If query error: show it
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Query Error", str(error))
            return

    def close_submenu(self):
        '''
        Closes the new order submenu and shows the previous menu.
        '''
        # Empty the order
        self.clear_order()
        self.destroy()  # Destroy the submenu
        self.master.deiconify()  # Show the main menu


class ViewOrderSubmenu(tk.Toplevel):
    '''
    Represents the view order submenu of the POS System.

    Inherits from tk.Toplevel class.

    Methods:
    - __init__: Initializes the ViewOrderSubmenu object.
    - fetch_orders: Fetches the orders from the database based on status.
    - display_orders: Displays the orders in a treeview.
    - close_submenu: Closes the view order submenu and shows the previous menu.
    '''

    def __init__(self, parent):
        '''
        Initializes the ViewOrderSubmenu object.

        Sets the window title, background color, and maximizes the window.
        Creates a tabbed layout for open and closed orders.
        Fetches and displays open and closed orders.
        '''
        super().__init__(parent)
        self.title("POS System")
        self.configure(background='#C0D5B2')
        self.state("zoomed")

        # Create a tabbed layout
        tab_control = ttk.Notebook(self)

        open_orders_tab = ttk.Frame(tab_control)
        closed_orders_tab = ttk.Frame(tab_control)

        tab_control.add(open_orders_tab, text="Open Orders")
        tab_control.add(closed_orders_tab, text="Closed Orders")

        tab_control.pack(expand=True, fill=tk.BOTH)

        # Fetch and display open orders
        open_orders = self.fetch_orders("open")
        self.display_orders(open_orders, open_orders_tab)

        # Fetch and display closed orders
        closed_orders = self.fetch_orders("closed")
        self.display_orders(closed_orders, closed_orders_tab)

        # Back button
        button_back = tk.Button(self, text="Back to Main Menu", command=self.close_submenu)
        button_back.pack(padx=10, pady=5)

    def fetch_orders(self, status):
        '''
        Fetches the orders from the database based on the status.

        Args:
        - status: The status of the orders to fetch ("open" or "closed").

        Returns:
        - orders: A list of orders fetched from the database.
        '''
        try:
            query = f"SELECT table_id, menu_item_name, price, quantity \
                    FROM get_todays_orders() WHERE status = '{status}'"
            
            orders = SQL_query(query)
            return orders
        except (Exception, psycopg2.Error) as error:
            # Handle any errors that occur during the execution
            print(f"An error occurred: {str(error)}")
            return

    def display_orders(self, orders, tab):
        '''
        Displays the orders in a treeview on the specified tab.

        Args:
        - orders: A list of orders to display.
        - tab: The tab where the orders should be displayed.
        '''
        if orders:
            self.treeview = ttk.Treeview(tab, columns=("Menu Item", "Price", "Quantity"))
            self.treeview.heading("#0", text="Table Number")
            self.treeview.heading("#1", text="Menu Item")
            self.treeview.heading("#2", text="Price")
            self.treeview.heading("#3", text="Quantity")

            for order in orders:
                self.treeview.insert("", tk.END, text=order[0], values=order[1:])

            self.treeview.pack(expand=True, fill=tk.BOTH)
        else:
            label_no_orders = tk.Label(tab, text="No orders found.")
            label_no_orders.pack(padx=10, pady=10)

    def close_submenu(self):
        '''
        Closes the view order submenu and shows the previous menu.

        Closes the database connection and destroys the submenu.
        '''
        # Close the database connection and destroy the submenu
        
        self.destroy()
        self.master.deiconify()  # Show the main menu


class StockSubmenu(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Stock Submenu")
        self.configure(background='#C0D5B2')
        self.state("zoomed")
        
        self.treeview = ttk.Treeview(self, columns=("Ingredient Name", "Expiry Date", "Quantity", "Units"))
        self.treeview.heading("#0", text="Ingredient ID")
        self.treeview.heading("#1", text="Ingredient Name")
        self.treeview.heading("#2", text="Expiry Date")
        self.treeview.heading("#3", text="Quantity")
        self.treeview.heading("#4", text="Units")
        self.treeview.pack(expand=True, fill=tk.BOTH)
        
        self.display_stock()
        
        # Back button
        button_back = tk.Button(self, text="Back to Main Menu", command=self.close_submenu)
        button_back.pack(padx=10, pady=5)

    def display_stock(self):
        """
        Fetches and displays the current stock data in the Treeview widget.
        """
        try:
            query = """
                SELECT cs.ingredient_id, i.ingredient_name, cs.expiry_date, cs.quantity, cs.units
                FROM "Current_stock" cs
                INNER JOIN "Ingredient" i ON cs.ingredient_id = i.ingredient_id
            """
            stock_data = SQL_query(query)

            for stock in stock_data:
                ingredient_id, ingredient_name, expiry_date, quantity, units = stock
                self.treeview.insert("", tk.END, text=ingredient_id, 
                                     values=(ingredient_name, expiry_date, quantity, units))
        except (Exception, psycopg2.Error) as error:
            # Handle any errors that occur during the execution
            print(f"An error occurred: {str(error)}")
            return

    def close_submenu(self):
        """
        Closes the submenu and shows the main menu.
        """
        self.destroy()
        self.master.deiconify()  # Show the main menu



class PaymentSubmenu(tk.Toplevel):
    '''
    Represents the payment submenu of the POS System.

    Inherits from tk.Toplevel class.

    Methods:
    - __init__: Initializes the PaymentSubmenu object.
    - reset_totals: Resets the total amounts to zero.
    - show_totals: Displays the total amounts in the treeview.
    - update_checkboxes: Updates the checkboxes and orders based on the selected table.
    - get_open_tables_numbers: Retrieves the numbers of open tables.
    - fetch_order: Fetches the order for a specific table.
    - process_payment_items: Processes the payment for selected items.
    - process_payment_all: Processes the payment for the entire table.
    - close_submenu: Closes the payment submenu and shows the previous menu.
    '''

    def __init__(self, parent):
        '''
        Initializes the PaymentSubmenu object.

        Sets the window title, background color, and maximizes the window.
        Creates a dropdown menu for table selection.
        Creates a treeview to display payment information.
        Creates buttons for refreshing totals and processing payment.
        Creates a label for displaying the total amount.
        '''
        super().__init__(parent)
        self.title("Payment Submenu")
        self.configure(background='#C0D5B2')
        self.state("zoomed")

        self.total_names = ['Full order total', 'Select items total']

        # New payment
        self.default_option_table = "Select a table number"  # Default option for table dropdown menu
        # The selected table will be shown as a string
        self.selected_table = tk.StringVar(self)
        # List of tables
        table_list = self.get_open_tables_numbers()
        # Create Dropdown menu for table selection
        drop = tk.OptionMenu(self, self.selected_table, *table_list, command=self.update_checkboxes)
        drop.pack(pady=40)

        self.checkboxes_frame = tk.Frame(self)
        self.checkboxes_frame.pack()

        self.treeview = ttk.Treeview(self, columns=("Total", "Amount"))
        self.treeview.heading("#0", text="Total")
        self.treeview.heading("#1", text="Amount")
        self.treeview.pack(expand=True, fill=tk.BOTH)

        # Create a button to calculate the total and process the payment
        button_refresh_totals = tk.Button(self, text="Refresh Totals", command=self.show_totals)
        button_refresh_totals.pack(pady=10)

        button_pay = tk.Button(self, text="Pay Items", command=self.process_payment_items)
        button_pay.pack(pady=10)

        button_pay_all = tk.Button(self, text="Pay All", command=self.process_payment_all)
        button_pay_all.pack(pady=10)

        # Create a label to display the total amount
        self.label_total = tk.Label(self, text="")
        self.label_total.pack()

        # Back button
        button_back = tk.Button(self, text="Back to Main Menu", command=self.close_submenu)
        button_back.pack(padx=10, pady=5)

    def reset_totals(self):
        '''
        Resets the total amounts to zero.
        '''
        self.total = 0
        self.selected_total = 0

    def show_totals(self):
        '''
        Displays the total amounts in the treeview.

        Calculates the total and selected total amounts based on the checkboxes.
        Inserts the total amounts into the treeview.
        '''
        # Clear the existing totals in the treeview
        self.reset_totals()
        self.treeview.delete(*self.treeview.get_children())

        prices = [float(item[1][1:]) for item in self.orders]

        self.total = sum(prices)

        for box, price in zip(self.item_vars, prices):
            if box.get() == 1:
                self.selected_total += price

        totals_zipped = zip(self.total_names, [self.total, self.selected_total])

        for t in reversed(list(totals_zipped)):
            name, amount = t

            amount = '£' + str(round(amount, 2))
            self.treeview.insert("", tk.END, text=name, values=amount)

    def update_checkboxes(self, selected_table):
        '''
        Updates the checkboxes and orders based on the selected table.

        Resets the totals, clears existing checkboxes, and fetches the orders for the selected table.
        Creates checkboxes for each menu item in the orders.
        '''
        # Reset totals
        self.reset_totals()

        # Clear existing checkboxes
        for checkbox in self.checkboxes_frame.winfo_children():
            checkbox.destroy()

        # Fetch the orders for the selected table
        self.orders = self.fetch_order(int(selected_table.split(" ")[-1]))

        # Create a checkbox for each menu item in the orders
        self.item_vars = []
        for item in self.orders:
            menu_item_name = item[0]  # Extract the menu item name from the fetched orders
            var = tk.IntVar()
            self.item_vars.append(var)
            checkbox = tk.Checkbutton(self.checkboxes_frame, text=menu_item_name, variable=var)
            checkbox.pack(anchor=tk.W)

    def get_open_tables_numbers(self):
        '''
        Retrieves the numbers of open tables.

        Connects to the database and executes a query to select table numbers with open orders.
        Returns a list of table numbers.
        '''
        table_numbers = []
        try:
            # Execute the SQL query to select table numbers where they have open orders
            select_query = f"SELECT distinct(table_id) FROM get_todays_orders() WHERE status = 'open'"
            
            # Return these to a list
            open_orders = SQL_query(select_query)

            # Extract as list of ints
            table_numbers = ['Table ' + str(t_num[0]) for t_num in open_orders]

            return table_numbers
        except (Exception, psycopg2.Error) as error:
            # Handle any errors that occur during the execution
            print(f"An error occurred: {str(error)}")

    def fetch_order(self, table_num):
        '''
        Fetches the order for a specific table.

        Connects to the database and executes a query to select the menu item name, price, 
        and quantity for the given table.
        Returns a list of orders.
        '''
        if not isinstance(table_num, int):
            return []

        try:
            #SQL query to find order detials on a table
            query = f"SELECT menu_item_name, price, quantity FROM get_todays_orders() \
                  WHERE status = 'open' and table_id = {table_num}"
            
            #Execute and retun the query
            order_details = SQL_query(query)
            return order_details
        except (Exception, psycopg2.Error) as error:
            # Handle any errors that occur during the execution
            print(f"An error occurred: {str(error)}")
            return

    def process_payment_items(self):
        '''
        Processes the payment for selected items.
        '''
        #TODO: -> Add payment processing here
        pass

    def process_payment_all(self):
        '''
        Processes the payment for the entire table.
        '''
        #TODO: -> Add payment processing here
        pass

    def close_submenu(self):
        '''
        Closes the payment submenu and shows the previous menu.

        Closes the database connection and destroys the submenu.
        '''
        self.destroy()
        self.master.deiconify()  # Show the main menu



class TableAssignmentSubmenu(tk.Toplevel):
    '''
    Represents the table assignment submenu of the POS System.

    Inherits from tk.Toplevel class.

    Methods:
    - __init__: Initializes the TableAssignmentSubmenu object.
    - assign_tables: Assigns a table to a group and reflects this in the DB as a booking.
    - clear_tables: clears the current list of selected tables
    - find_tables: finds a list of free tables for the group
    - close_submenu: Closes the table assignment submenu and shows the previous menu.

    '''

    #TODO -> Add treeview to show option of assigned table ids and capactities
    # -> Add function to add booking to db
    # Maybe try to change to only assign tables close together?

    def __init__(self, parent):
        '''
        Initializes the TableAssignmentSubmenu object.

        Sets the window title, background color, and maximizes the window.
        Creates input fields for group size, duration, and start time.
        Creates a button to assign the table.

        TODO -> change start_time to be dropdown menu instead of text field, one for date one for times.
        '''
        super().__init__(parent)
        self.title("Table Assignment Submenu")
        self.configure(background='#C0D5B2')
        self.state("zoomed")

        # Clear selected tables
        self.clear_tables()

        # Group size field
        label_group_size = tk.Label(self, text="Group Size:")
        label_group_size.pack(padx=10, pady=10)
        self.entry_group_size = tk.Entry(self)
        self.entry_group_size.pack(padx=10, pady=5)

        # Duration field
        label_duration = tk.Label(self, text="Duration (in hours):")
        label_duration.pack(padx=10, pady=10)
        self.entry_duration = tk.Entry(self)
        self.entry_duration.pack(padx=10, pady=5)

        # Start time field
        label_start_time = tk.Label(self, text="Start Time (YYYY-MM-DD HH:MM:SS):")
        label_start_time.pack(padx=10, pady=10)
        self.entry_start_time = tk.Entry(self)
        self.entry_start_time.pack(padx=10, pady=5)

        # Find button
        button_find = tk.Button(self, text="Find Table(s)", command=self.find_tables)
        button_find.pack(padx=10, pady=5)

        # Confirm assignment button
        button_assign = tk.Button(self, text="Confirm Table(s)", command=self.assign_tables)
        button_assign.pack(padx=10, pady=5)

        # Back button
        button_back = tk.Button(self, text="Back to Main Menu", command=self.close_submenu)
        button_back.pack(padx=10, pady=5)

    def find_tables(self):
        '''
        Assigns a table to a group.

        Retrieves the group size, duration, and start time from the input fields.
        Calls the `table_assignment` function to assign the table.
        Displays a success message box if the assignment is successful.
        '''
        self.group_size = self.entry_group_size.get()
        self.duration = self.entry_duration.get()
        self.start_time = self.entry_start_time.get()

        if not self.group_size:
            messagebox.showerror("Input Error", "Please enter both the group size")
            return

        if not self.start_time:
            self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not self.duration:
            self.duration = '2 hours'

        try:
            tables = find_available_tables(self.start_time, str(self.duration)+ " hours")
            self.selected_tables = table_assigner(available_tables= tables, party_size= int(self.group_size))
            messagebox.showinfo("Table Assignment",
                                 f"Table(s) found: \
                                    {', '.join(str(table_id) for table_id in self.selected_tables)}.")
            self.entry_group_size.delete(0, 'end')
            self.entry_duration.delete(0, 'end')
            self.entry_start_time.delete(0, 'end')
        except Exception as e:
            messagebox.showerror("Table Assignment Error", str(e))

    def assign_tables(self):
        '''
        Assigns table as booking in db
        #TODO -> add table booking section
        '''
        if len(self.selected_tables) == 0:
            messagebox.showerror("Table Assignment Error", "No selected tables.")
            return
        try:
            # SQL query to insert a booking
            query = f"SELECT insert_booking(ARRAY{self.selected_tables}, \
                                            {self.group_size}, \
                                            '{self.start_time}', \
                                            '{self.duration}');"
            
            # Add the new booking to the database
            SQL_query(query, to_return_rows=False)

        except (Exception, psycopg2.Error) as error:
            # Handle any errors that occur during the execution
            print(f"An error occurred: {str(error)}")
            return
        
    def clear_tables(self):
        '''
        Clear the list of selected table ids.
        '''
        self.selected_tables = []


    def close_submenu(self):
        '''
        Closes the table assignment submenu and shows the previous menu.
        '''
        self.destroy()
        self.master.deiconify()  # Show the main menu



if __name__ == "__main__":
    window = WelcomeWindow()
    window.mainloop()
