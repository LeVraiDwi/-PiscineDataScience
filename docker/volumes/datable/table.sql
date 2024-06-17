create type EventType as enum (
    'view',
    'cart',
    'remove_from_cart',
    'purchase'
);

BEGIN TRANSACTION;
do 
$$
begin
    create TABLE data_2022_oct (event_time timestamptz, event_type EventType, product_id int, price float, user_id int8, user_session varchar(255));
    copy data_2022_oct (event_time, event_type, product_id, price, user_id, user_session) FROM '/tmp/data_2022_oct.csv' DELIMITER ',' CSV HEADER;
end; 
$$;
COMMIT TRANSACTION;