/*
Use this to drop all tables to reset

CREATE OR REPLACE FUNCTION drop_all_tables()
  RETURNS VOID
AS $$
DECLARE
  table_name_var TEXT;
BEGIN
  -- Get the names of all tables in the current schema
  FOR table_name_var IN (SELECT table_name FROM information_schema.tables WHERE table_schema = current_schema())
  LOOP
    -- Construct the DROP TABLE statement for each table and execute it
    EXECUTE 'DROP TABLE IF EXISTS "' || table_name_var || '" CASCADE;';
  END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT drop_all_tables();
*/


--Create employee table
CREATE TABLE IF NOT EXISTS "employee" (
  employee_id SERIAL PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  job_title TEXT,
  employment_type TEXT, --full time or part TIME
  employee_email TEXT,
  employee_phone VARCHAR(20),
  employee_address VARCHAR (50),
  employee_DOB DATE,
  employee_gender TEXT
);

-- Create the table_number table
CREATE TABLE IF NOT EXISTS "table_number" (
  table_id SERIAL PRIMARY KEY,
  capacity INT
);

-- Create the order table
CREATE TABLE IF NOT EXISTS "order" (
  order_id SERIAL PRIMARY KEY,
  time_ordered TIMESTAMP,
  time_delivered TIMESTAMP,
  table_id INT,
  employee_id INT,
  FOREIGN KEY (table_id) REFERENCES "table_number" (table_id),
  FOREIGN KEY (employee_id) REFERENCES "employee" (employee_id)
);

-- Create the booking table
CREATE TABLE "booking" (
  booking_id SERIAL PRIMARY KEY,
  booking_name TEXT,
  group_size INT,
  contact_phone VARCHAR(20),
  contact_email TEXT,
  start_time TIMESTAMP,
  duration INTERVAL DEFAULT ('1.5 hours'), --Cannot do end_time as cannot reference start time for default
  table_id INT,
  comments VARCHAR(100),
  FOREIGN KEY (table_id) REFERENCES "table_number" (table_id)
);

--Create payment table
CREATE TABLE IF NOT EXISTS "payment" (
  payment_id SERIAL PRIMARY KEY,
  order_id INT,
  payment_method TEXT,
  amount MONEY,
  payment_time TIMESTAMP,
  FOREIGN KEY (order_id)  REFERENCES "order" (order_id)
);

--Create payroll table
CREATE TABLE IF NOT EXISTS "payroll" (
  salary_id SERIAL PRIMARY KEY,
  employee_id INT,
  year INT,
  month VARCHAR(10),
  hours_worked FLOAT,
  hourly_rate FLOAT,
  FOREIGN KEY (employee_id)  REFERENCES "employee" (employee_id)
);

-- Create the menu_item table
CREATE TABLE IF NOT EXISTS "menu_item" (
  menu_item_id SERIAL PRIMARY KEY,
  menu_item_name TEXT,
  price MONEY,
  category TEXT
);

-- Create the order_item table
CREATE TABLE IF NOT EXISTS "order_item" (
  order_id INT,
  menu_item_id INT,
  quantity INT,
  comments VARCHAR(100),
  PRIMARY KEY (order_id, menu_item_id),
  FOREIGN KEY (order_id) REFERENCES "order" (order_id),
  FOREIGN KEY (menu_item_id) REFERENCES "menu_item" (menu_item_id)
);


/*-- Create link table between booking and table_number
CREATE TABLE "BookingLinkTableNumber" (
  booking_id INT,
  table_id INT,
  PRIMARY KEY (booking_id, table_id),
  FOREIGN KEY (booking_id) REFERENCES "booking" (booking_id),
  FOREIGN KEY (table_id) REFERENCES "table_number" (table_id)
);
*/ -- Probably not needed

--Create supplier table
CREATE TABLE IF NOT EXISTS "supplier" (
  supplier_id SERIAL PRIMARY KEY,
  supplier_name TEXT,
  supplier_address TEXT,
  supplier_phone TEXT,
  supplier_email TEXT
);

-- Create ingredient table
CREATE TABLE IF NOT EXISTS "ingredient" (
  ingredient_id SERIAL PRIMARY KEY,
  ingredient_name TEXT,
  supplier_quantity TEXT,
  low_threshold INT,
  unit TEXT,
  low_threshold_grams INT,
  supplier_id INT,
  FOREIGN KEY (supplier_id) REFERENCES "supplier" (supplier_id)
);

--Create recipe table
CREATE TABLE "recipe" (
  menu_item_id INT,
  ingredient_id INT,
  quantity NUMERIC,
  PRIMARY KEY (menu_item_id, ingredient_id),
  FOREIGN KEY (menu_item_id) REFERENCES "menu_item" (menu_item_id),
  FOREIGN KEY (ingredient_id) REFERENCES "ingredient" (ingredient_id)
);

-- Create allergen table
CREATE TABLE IF NOT EXISTS "allergen" (
  allergen_id SERIAL PRIMARY KEY,
  allergen_name TEXT
);

-- Create ingredient_allergen table
CREATE TABLE "ingredient_allergen" (
  ingredient_id INT,
  allergen_id INT,
  PRIMARY KEY (ingredient_id, allergen_id),
  FOREIGN KEY (ingredient_id) REFERENCES "ingredient" (ingredient_id),
  FOREIGN KEY (allergen_id) REFERENCES "allergen" (allergen_id)
);

--Create (storage) location table 
CREATE TABLE IF NOT EXISTS "location" (
  location_id SERIAL PRIMARY KEY,
  location_name TEXT
); 

-- Create current_stock table
CREATE TABLE IF NOT EXISTS "current_stock" (
  ingredient_id INT,
  location_id INT,
  delivery_date DATE,
  total_cost MONEY,
  expiry_date DATE,
  quantity NUMERIC,
  PRIMARY KEY (ingredient_id, expiry_date, location_id, total_cost),
  FOREIGN KEY (ingredient_id) REFERENCES "ingredient" (ingredient_id),
  FOREIGN KEY (location_id) REFERENCES "location" (location_id)
);








  
  







