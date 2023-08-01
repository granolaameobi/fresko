CREATE OR REPLACE FUNCTION update_current_stock()
RETURNS TRIGGER AS $$
DECLARE
    item RECORD;
BEGIN
    -- Loop through each item in the order
    FOR item IN SELECT * FROM "order_item" WHERE order_id = NEW.order_id LOOP
        -- Update the current stock for each ingredient in the recipe
        UPDATE "current_stock"
        SET quantity = quantity - (item.quantity * recipe.quantity)
        FROM "recipe"
        WHERE "current_stock".ingredient_id = recipe.ingredient_id
        AND recipe.menu_item_id = item.menu_item_id;
    END LOOP;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_order_placed
AFTER INSERT ON "order"
FOR EACH ROW
EXECUTE FUNCTION update_current_stock();



--check if any ingredient qunatity is less than the threshold
CREATE OR REPLACE FUNCTION stock_check()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.quantity < NEW.low_threshold THEN
        RAISE EXCEPTION 'Ingredient % needs resupply', NEW.ingredient_name;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


--Activates after the stock is updated e.g. an order cooked
CREATE TRIGGER stock_check_trigger
AFTER UPDATE ON current_stock
FOR EACH ROW
EXECUTE FUNCTION stock_check();

