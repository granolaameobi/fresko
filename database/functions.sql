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
BEGIN
  -- Insert a new order into the "Order" table
  INSERT INTO "Order" (time_ordered, time_delivered, table_id)
  VALUES (NOW(), NULL, p_table_id)
  RETURNING order_id INTO new_order_id;

  -- Determine the length of the input arrays
  array_length := array_length(p_menu_item_ids, 1);

  -- Insert order items into the "OrderItem" table for each menu item
  FOR i IN 1..array_length
  LOOP
    INSERT INTO "OrderItem" (order_id, menu_item_id, quantity)
    VALUES (new_order_id, p_menu_item_ids[i], p_quantities[i]);
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
      "Order" o
    INNER JOIN
      "OrderItem" oi ON o.order_id = oi.order_id
    INNER JOIN
      "MenuItem" mi ON oi.menu_item_id = mi.menu_item_id
	LEFT JOIN
      "Payment" pa ON o.order_id = pa.order_id
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

