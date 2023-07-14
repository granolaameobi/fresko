
DELETE FROM "Menu_item";
-- Insert dummy data into the MenuItem table
INSERT INTO "Menu_item" (menu_item_name, price, course, available)
VALUES
  ('Chicken Gyros', 9.00, 'main', '1'),
  ('Pork Gyros', 9.00, 'main', '1'),
  ('Lamb Gyros', 9.50, 'main', '1'),
  ('Halloumi Gyros', 9.50, 'main', '1'),
  ('Falafel Gyros', 9.50, 'main', '1'),
  ('Chicken Souvlaki', 12.00, 'main', '1'),
  ('Pork Souvlaki', 12.00, 'main', '1'),
  ('Lamb Souvlaki', 12.50, 'main', '1'),
  ('Chicken Fresko', 12.00, 'main', '1'),
  ('Lamb Fresko', 12.50, 'main', '1'),
  ('The Greek', 10.50, 'starter', '1'),
  ('The Medi', 9.00, 'main', '1'),
  ('Green soda', 2.00, 'drink', '1'),
  ('Water', 1.50, 'drink', '1'),
  ('Hummus', 1.00, 'side', '1'),
  ('Tzatziki', 1.00, 'side', '1'),
  ('Tahini sauce', 1.00, 'side', '1'),
  ('Mint yoghurt sauce', 1.00, 'side', '1'),
  ('Falafel', 1.50, 'side', '1'),
  ('Halloumi', 1.50, 'side', '1'),
  ('Crumbled feta', 1.50, 'side', '1'),
  ('Pita', 2.00, 'side', '1'),
  ('Oregano chips', 2.00, 'side', '1'),
  ('Extra skewer', 3.00, 'side', '1');

--Clear TABLE
DELETE FROM "Supplier"; 
-- Dummy data to match ingerdietns
INSERT INTO "Supplier" (supplier_id, supplier_name, supplier_address, supplier_phone, supplier_email)
VALUES
  (058, 'Stream foods', '131-138 Westbourne Park, Derby, Derbyshire', '1632960208', 'streamfoods@email.com'),
  (081, 'Supplier B', 'Address B', 'Phone B', 'emailB@example.com'),
  (082, 'Supplier C', 'Address C', 'Phone C', 'emailC@example.com');

-- clear table
DELETE FROM "Ingredient";
--Add dummy values
INSERT INTO "Ingredient" (ingredient_id, ingredient_name, low_threshold, unit, supplier_id)
VALUES
  (351, 'Chickpea Flour', 0.3, 'kg', 058),
  (352, 'Olive Oil', 0.2, 'L', 058),
  (353, 'Garlic', 0.1, 'kg', 058),
  (354, 'Onion', 0.2, 'kg', 058),
  (355, 'Tomato', 0.3, 'kg', 058),
  (356, 'Cucumber', 0.2, 'kg', 058),
  (357, 'Lettuce', 0.1, 'kg', 058),
  (358, 'Yogurt', 0.5, 'kg', 058),
  (359, 'Lemon Juice', 0.2, 'L', 058),
  (360, 'Pita Bread', 0.4, 'kg', 058),
  (361, 'Cumin', 0.05, 'kg', 058),
  (362, 'Paprika', 0.05, 'kg', 058),
  (363, 'Salt', 0.1, 'kg', 058),
  (364, 'Pepper', 0.05, 'kg', 058),
  (365, 'Parsley', 0.1, 'kg', 058),
  (366, 'Mint', 0.05, 'kg', 058),
  (367, 'Sugar', 0.2, 'kg', 058),
  (368, 'Vinegar', 0.3, 'L', 058),
  (369, 'Chicken', 0.8, 'kg', 081),
  (370, 'Beef', 0.9, 'kg', 082);
 
--Clear table
DELETE FROM "Location";
-- Dummy data
INSERT INTO "Location" (location_id, location_name)
VALUES
  (8, 'Freezer'); 
 
--Clear TABLE
DELETE FROM "Current_stock";
--Dummy data matching ingredients
INSERT INTO "Current_stock" (ingredient_id, location_id, expiry_date, total_cost, delivery_date, quantity)
VALUES
  (351, 8, '2023-09-18', 320.54, '2023-07-01', 110),
  (352, 8, '2023-10-12', 220.98, '2023-07-02', 95),
  (353, 8, '2023-11-05', 180.75, '2023-07-03', 85),
  (354, 8, '2023-09-25', 280.21, '2023-07-04', 100),
  (355, 8, '2023-10-18', 340.67, '2023-07-05', 120),
  (356, 8, '2023-10-02', 200.33, '2023-07-06', 90),
  (357, 8, '2023-09-22', 150.89, '2023-07-07', 75),
  (358, 8, '2023-11-15', 260.44, '2023-07-08', 80),
  (359, 8, '2023-09-28', 320.54, '2023-07-09', 105),
  (360, 8, '2023-10-08', 280.21, '2023-07-10', 115),
  (361, 8, '2023-11-05', 220.98, '2023-07-11', 70),
  (362, 8, '2023-09-20', 180.75, '2023-07-12', 60),
  (363, 8, '2023-10-12', 240.32, '2023-07-13', 80),
  (364, 8, '2023-10-01', 140.43, '2023-07-14', 50),
  (365, 8, '2023-09-23', 210.54, '2023-07-15', 70),
  (366, 8, '2023-10-05', 120.65, '2023-07-16', 40),
  (367, 8, '2023-11-10', 180.75, '2023-07-17', 90),
  (368, 8, '2023-09-29', 240.32, '2023-07-18', 100),
  (369, 8, '2023-10-15', 160.87, '2023-07-19', 75),
  (370, 8, '2023-09-27', 190.98, '2023-07-20', 85);
  

  
  
/*  
-- select * from "Table_number";
  
  
-- Insert dummy data into the TableNumber table
INSERT INTO "Table_number" (capacity)
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




-- Call the function to create dummy orders for all table IDs
SELECT create_dummy_order();
*/