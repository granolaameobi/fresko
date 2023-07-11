/*
Use this to drop all tables to reset
*/
SELECT drop_all_tables();


-- Create the TableNumber table
CREATE TABLE IF NOT EXISTS "TableNumber" (
  table_id SERIAL PRIMARY KEY,
  capacity INT
);

-- Create the Order table
CREATE TABLE IF NOT EXISTS "Order" (
  order_id SERIAL PRIMARY KEY,
  time_ordered TIMESTAMP,
  time_delivered TIMESTAMP,
  table_id INT,
  FOREIGN KEY (table_id) REFERENCES "TableNumber" (table_id)
);

CREATE TABLE IF NOT EXISTS "Payment" (
  payment_id SERIAL PRIMARY KEY,
  order_id INT,
  payment_method TEXT,
  amount MONEY,
  payment_time TIMESTAMP,
  FOREIGN KEY (order_id)  REFERENCES "Order" (order_id)
);

-- Create the MenuItem table
CREATE TABLE IF NOT EXISTS "MenuItem" (
  menu_item_id SERIAL PRIMARY KEY,
  menu_item_name TEXT,
  price MONEY
);

-- Create the OrderItem table
CREATE TABLE IF NOT EXISTS "OrderItem" (
  order_id INT,
  menu_item_id INT,
  quantity INT,
  PRIMARY KEY (order_id, menu_item_id),
  FOREIGN KEY (order_id) REFERENCES "Order" (order_id),
  FOREIGN KEY (menu_item_id) REFERENCES "MenuItem" (menu_item_id)
);

-- Create the Booking table
CREATE TABLE "Booking" (
  booking_id SERIAL PRIMARY KEY,
  booking_name TEXT,
  group_size INT,
  contact_phone VARCHAR(20),
  contact_email TEXT,
  start_time TIMESTAMP,
  duration INTERVAL DEFAULT ('1.5 hours') --Cannot do end_time as cannot reference start time for default
);

-- Create link table between Booking and TableNumber
CREATE TABLE "BookingLinkTableNumber" (
  booking_id INT,
  table_id INT,
  PRIMARY KEY (booking_id, table_id),
  FOREIGN KEY (booking_id) REFERENCES "Booking" (booking_id),
  FOREIGN KEY (table_id) REFERENCES "TableNumber" (table_id)
);


-- Create Allergens table
CREATE TABLE IF NOT EXISTS "Allergen" (
  allergen_id SERIAL PRIMARY KEY,
  allergen_name TEXT
);


--Create Supplier table
CREATE TABLE IF NOT EXISTS "Supplier" (
  supplier_id SERIAL PRIMARY KEY,
  supplier_name TEXT,
  address TEXT,
  conact_number TEXT,
  email TEXT
);

-- Creat Ingredients table
CREATE TABLE IF NOT EXISTS "Ingredient" (
  ingredient_id SERIAL PRIMARY KEY,
  ingredient_name TEXT,
  low_threshold INT,
  supplier_id INT,
  FOREIGN KEY (supplier_id) REFERENCES "Supplier" (supplier_id)
);

-- Create Ingredient Allergens table
CREATE TABLE "IngredientAllergen" (
  ingredient_id INT,
  allergen_id INT,
  PRIMARY KEY (ingredient_id, allergen_id),
  FOREIGN KEY (ingredient_id) REFERENCES "Ingredient" (ingredient_id),
  FOREIGN KEY (allergen_id) REFERENCES "Allergen" (allergen_id)
);

--Create Recipe table
CREATE TABLE "Recipe" (
  menu_item_id INT,
  ingredient_id INT,
  quantity NUMERIC,
  PRIMARY KEY (menu_item_id, ingredient_id),
  FOREIGN KEY (menu_item_id) REFERENCES "MenuItem" (menu_item_id),
  FOREIGN KEY (ingredient_id) REFERENCES "Ingredient" (ingredient_id)
);

--Create (storage) Locations table 
CREATE TABLE IF NOT EXISTS "Location" (
  location_id SERIAL PRIMARY KEY,
  location_name TEXT
); 

-- Create Current Stock table
CREATE TABLE IF NOT EXISTS "CurrentStock" (
  ingredient_id INT,
  expiry_date DATE,
  location_id INT,
  total_cost MONEY,
  delivery_date DATE,
  quantity NUMERIC,
  units TEXT,
  PRIMARY KEY (ingredient_id, expiry_date, location_id, total_cost),
  FOREIGN KEY (ingredient_id) REFERENCES "Ingredient" (ingredient_id),
  FOREIGN KEY (location_id) REFERENCES "Location" (location_id)
);





  
  







