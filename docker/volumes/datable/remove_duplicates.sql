BEGIN TRANSACTION;
do
$$
begin
    create TABLE tmp as with remove_duplicates as (
        SELECT *, LAG(event_time) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevTime 
        FROM customers)
    SELECT event_time, event_type, product_id, price, user_id, user_session
    FROM remove_duplicates
    where event_time - prevTime > INTERVAL '1 second' or prevTime IS NULL;

    DROP TABLE customers;
    alter TABLE tmp RENAME TO customers;
end;
$$;
COMMIT TRANSACTION;