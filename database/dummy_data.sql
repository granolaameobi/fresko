-- Insert dummy data into the MenuItem table
INSERT INTO "MenuItem" (menu_item_name, price)
VALUES
  ('Burger', 9.99),
  ('Pizza', 12.99),
  ('Salad', 7.99),
  ('Pasta', 10.99),
  ('Steak', 18.99);
  
  
-- Insert dummy data into the TableNumber table
INSERT INTO "TableNumber" (capacity)
VALUES
  (2),
  (4),
  (6),
  (2),
  (4),
  (6),
  (8),
  (4),
  (2);


--Dummy orders
SELECT create_new_order(
  ARRAY[1, 2, 3], -- Array of menu_item_ids
  ARRAY[2, 1, 1], -- Array of quantities
  1 -- Table ID
);

SELECT create_new_order(
  ARRAY[4, 5], -- Array of menu_item_ids
  ARRAY[3, 1], -- Array of quantities
  2 -- Table ID
);

SELECT create_new_order(
  ARRAY[3, 1, 2], -- Array of menu_item_ids
  ARRAY[2, 2, 1], -- Array of quantities
  3 -- Table ID
);

SELECT create_new_order(
  ARRAY[5, 1, 4], -- Array of menu_item_ids
  ARRAY[1, 3, 2], -- Array of quantities
  4 -- Table ID
);

SELECT create_new_order(
  ARRAY[2, 3], -- Array of menu_item_ids
  ARRAY[1, 1], -- Array of quantities
  5 -- Table ID
);

SELECT create_new_order(
  ARRAY[1, 5, 2], -- Array of menu_item_ids
  ARRAY[3, 1, 2], -- Array of quantities
  6 -- Table ID
);

SELECT create_new_order(
  ARRAY[4, 3, 2, 1], -- Array of menu_item_ids
  ARRAY[1, 2, 1, 3], -- Array of quantities
  7 -- Table ID
);

SELECT create_new_order(
  ARRAY[1, 2], -- Array of menu_item_ids
  ARRAY[2, 1], -- Array of quantities
  8 -- Table ID
);

SELECT create_new_order(
  ARRAY[3, 4, 5], -- Array of menu_item_ids
  ARRAY[1, 2, 1], -- Array of quantities
  9 -- Table ID
);


-- -- Call the create_new_order function to create another order on each table
-- SELECT create_new_order(
--   ARRAY[2, 3, 4], -- Array of menu_item_ids
--   ARRAY[3, 2, 1], -- Array of quantities
--   1 -- Table ID
-- );

-- SELECT create_new_order(
--   ARRAY[1, 5], -- Array of menu_item_ids
--   ARRAY[2, 1], -- Array of quantities
--   2 -- Table ID
-- );

-- SELECT create_new_order(
--   ARRAY[1, 2, 3], -- Array of menu_item_ids
--   ARRAY[1, 1, 1], -- Array of quantities
--   3 -- Table ID
-- );

-- SELECT create_new_order(
--   ARRAY[4, 5], -- Array of menu_item_ids
--   ARRAY[1, 2], -- Array of quantities
--   4 -- Table ID
-- );

-- SELECT create_new_order(
--   ARRAY[2, 3, 5], -- Array of menu_item_ids
--   ARRAY[2, 1, 1], -- Array of quantities
--   5 -- Table ID
-- );

-- SELECT create_new_order(
--   ARRAY[1, 4], -- Array of menu_item_ids
--   ARRAY[3, 1], -- Array of quantities
--   6 -- Table ID
-- );

-- SELECT create_new_order(
--   ARRAY[5, 2, 3], -- Array of menu_item_ids
--   ARRAY[1, 2, 1], -- Array of quantities
--   7 -- Table ID
-- );

-- SELECT create_new_order(
--   ARRAY[1, 3], -- Array of menu_item_ids
--   ARRAY[2, 1], -- Array of quantities
--   8 -- Table ID
-- );

-- SELECT create_new_order(
--   ARRAY[4, 5], -- Array of menu_item_ids
--   ARRAY[1, 1], -- Array of quantities
--   9 -- Table ID
-- );

