BEGIN TRANSACTION;
do 
$$
begin
    alter table customer 
    add column category_id,
    add column category_code,
    add column brand;
    select * from customer JOIN items on customer.product_id = items.product_id order by customer.product_id;
    update customer set customer.category_id = items.category_id from items WHERE customer.product_id = items.product_id; 
end;
$$;
COMMIT TRANSACTION;