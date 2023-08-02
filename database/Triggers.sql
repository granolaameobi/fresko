-- --check if any ingredient qunatity is less than the threshold
CREATE OR REPLACE FUNCTION check_low_threshold()
RETURNS TRIGGER AS $$
DECLARE
  ingredient_rec RECORD;
BEGIN
  -- Check if any ingredient goes below the low threshold
  FOR ingredient_rec IN (
    SELECT ingredient_id, SUM(quantity) AS total_quantity
    FROM "current_stock"
    GROUP BY ingredient_id
  )
  LOOP
    IF ingredient_rec.total_quantity < (SELECT low_threshold FROM "ingredient" WHERE ingredient_id = ingredient_rec.ingredient_id) THEN
      -- Perform any action or raise a warning/log as needed
      RAISE NOTICE 'Ingredient % is below the low threshold!', ingredient_rec.ingredient_id;
    END IF;
  END LOOP;
  
  RETURN NULL; -- The trigger is after insert/update, so we don't need to change the inserted/updated row.
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE OR REPLACE TRIGGER check_low_threshold_trigger
AFTER INSERT OR UPDATE ON "current_stock"
FOR EACH STATEMENT
EXECUTE FUNCTION check_low_threshold();


