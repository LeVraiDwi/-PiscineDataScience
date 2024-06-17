BEGIN TRANSACTION;
do 
$$
declare
    t_name text;
begin
    create TABLE tmp (event_time timestamptz, event_type EventType, product_id int, price float, user_id int8, user_session varchar(255));
    insert into tmp (event_time, event_type, product_id, price, user_id, user_session) SELECT DISTINCT * FROM customer;
    DROP TABLE customer;
    ALTER TABLE tmp RENAME TO customer;
end; 
$$;
COMMIT TRANSACTION;