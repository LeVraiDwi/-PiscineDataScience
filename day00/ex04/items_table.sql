

BEGIN TRANSACTION;
do 
$$
declare
    me text;
    count int;
begin
    SET client_min_messages TO WARNING;
    CREATE TABLE items(product_id int, category_id int8, category_code varchar(255), brand varchar(255));
    copy items (product_id, category_id, category_code, brand) FROM '/tmp/item/item.csv' DELIMITER ',' CSV HEADER;
end;
$$;

COMMIT TRANSACTION;