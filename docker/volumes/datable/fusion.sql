BEGIN TRANSACTION;
do 
$$
begin

    update customer set category_id = t1.category_id, category_code = t1.category_code, brand = t1.brand from items t1 WHERE customer.product_id = t1.product_id; 
end;
$$;
COMMIT TRANSACTION;