/*
---------------------------------------------------------------------------------------------
Function to add a new order to the database more easily
-> TODO : Add trigger to update stock counts when this is called
*/
CREATE OR REPLACE FUNCTION create_new_order(
  p_menu_item_ids INT[],
  p_quantities INT[],
  p_table_id INT
) RETURNS INT
AS $$
DECLARE
  new_order_id INT;
  array_length INT;
  i INT;
  new_ingredient_id INT;
  ingredient_quantity_rec RECORD;
  new_ingredient_quantity NUMERIC;
BEGIN
  -- Insert a new order into the "Order" table
  INSERT INTO "order" (time_ordered, time_delivered, table_id)
  VALUES (NOW(), NULL, p_table_id)
  RETURNING order_id INTO new_order_id;

  -- Determine the length of the input arrays
  array_length := array_length(p_menu_item_ids, 1);

  -- Insert order items into the "OrderItem" table for each menu item
  FOR i IN 1..array_length
  LOOP
    INSERT INTO "Order_item" (order_id, menu_item_id, quantity)
    VALUES (new_order_id, p_menu_item_ids[i], p_quantities[i]);
    
    -- Update current stock for each ingredient used in the order
    FOR ingredient_quantity_rec IN (
      SELECT r.ingredient_id, r.quantity * p_quantities[i] AS ingredient_quantity
      FROM "recipe" AS r
      WHERE r.menu_item_id = p_menu_item_ids[i]
    )
    LOOP
      new_ingredient_id := ingredient_quantity_rec.ingredient_id;
      new_ingredient_quantity := ingredient_quantity_rec.ingredient_quantity;
      
      UPDATE "current_stock"
      SET quantity = quantity - new_ingredient_quantity
      WHERE ingredient_id = new_ingredient_id;
    END LOOP;
  END LOOP;

  -- Return the new order_id
  RETURN new_order_id;
END;
$$ LANGUAGE plpgsql;




/*
---------------------------------------------------------------------------------------------
Get todays orders
-> TODO : Change to get either open or closed orders (might have to split into two funcs)
*/

-- DROP FUNCTION get_todays_orders();
CREATE OR REPLACE FUNCTION get_todays_orders()
  RETURNS TABLE (
    order_id INT,
    table_id INT,
    menu_item_name TEXT,
    price MONEY,
    quantity INT,
	status TEXT
  )
AS $$
BEGIN
  RETURN QUERY
    SELECT
      o.order_id,
      o.table_id,
      mi.menu_item_name,
      mi.price,
      oi.quantity,
	  CASE
        WHEN pa.amount >= SUM(mi.price * oi.quantity) THEN 'closed'
        ELSE 'open'
      END AS status
    FROM
      "order" o
    INNER JOIN
      "order_item" oi ON o.order_id = oi.order_id
    INNER JOIN
      "menu_item" mi ON oi.menu_item_id = mi.menu_item_id
	LEFT JOIN
      "payment" pa ON o.order_id = pa.order_id
	WHERE
      DATE(o.time_ordered) = CURRENT_DATE
	GROUP BY
	  o.order_id,
      o.table_id,
      mi.menu_item_name,
	  mi.price,
      oi.quantity,
	  pa.amount
    ORDER BY
--       o.table_id,
      o.order_id desc;
END;
$$ LANGUAGE plpgsql;


/*
---------------------------------------------------------------------------------------------
To create a dummy order of 5-6 items on each table for testing
*/


-- Create the function
CREATE OR REPLACE FUNCTION create_dummy_orders()
RETURNS VOID AS $$
DECLARE
  table_id INT;
BEGIN
  -- Loop through table IDs
  FOR table_id IN SELECT DISTINCT "table_number".table_id FROM "table_number"
  LOOP
    -- Generate random menu_item_ids and quantities
    DECLARE
      menu_item_ids INT[] := ARRAY(SELECT menu_item_id FROM "menu_item" ORDER BY random() LIMIT floor(random() * 2) + 3);
      quantities INT[] := ARRAY(SELECT floor(random() * 3) + 1 FROM generate_series(1, array_length(menu_item_ids, 1)));
    BEGIN
      -- Create the order
      PERFORM create_new_order(menu_item_ids, quantities, table_id);
    END;
  END LOOP;
END;
$$ LANGUAGE plpgsql;

/*
---------------------------------------------------------------------------------------------
Insert booking on a table/list of tables
*/

-- Create the function
CREATE OR REPLACE FUNCTION insert_booking(
    new_table_ids INT[],
	new_group_size INT,
    new_start_time TIMESTAMP DEFAULT NULL,
    new_duration INTERVAL DEFAULT '1.5 hours',
    new_comment TEXT DEFAULT NULL
)
RETURNS VOID AS
$$
DECLARE
    table_id INT;
BEGIN
    -- Check if new_start_time is NULL and assign current timestamp if it is
    IF new_start_time IS NULL THEN
        new_start_time := now();
    END IF;

    -- Loop through each table ID in the list
    FOREACH table_id IN ARRAY new_table_ids
    LOOP
        -- Insert a new booking into the Booking table
        INSERT INTO "booking" (group_size, start_time, duration, table_id, comments)
        VALUES (new_group_size, new_start_time, new_duration, table_id, new_comment);
    END LOOP;
END;
$$
LANGUAGE plpgsql;



/*
---------------------------------------------------------------------------------------------
Get order total cost
*/

CREATE OR REPLACE FUNCTION get_order_total_cost(order_id_param INT) 
RETURNS MONEY AS
$$
DECLARE
    total_cost MONEY := 0;
BEGIN
    SELECT SUM(oi.quantity * mi.price)
    INTO total_cost
    FROM "order" o
    JOIN "order_item" oi ON o.order_id = oi.order_id
    JOIN "menu_item" mi ON oi.menu_item_id = mi.menu_item_id
    WHERE o.order_id = order_id_param;
    
    RETURN total_cost;
END;
$$
LANGUAGE plpgsql;






/*
---------------------------------------------------------------------------------------------
Clear database if want to reset tables
*/

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

