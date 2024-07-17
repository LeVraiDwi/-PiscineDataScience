BEGIN TRANSACTION;
do
$$
begin
    create TABLE tmp as with remove_duplicates as (
        SELECT *, LAG(event_time) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevTime,
        LAG(product_id) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevProduct,
        LAG(event_type) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevEvent_type
        FROM customers)
    SELECT event_time, event_type, product_id, price, user_id, user_session
    FROM remove_duplicates
    where prevEvent_type != event_type or prevProduct != product_id or prevTime IS NULL or event_time - prevTime > INTERVAL '1 second';

    DROP TABLE customers;
    alter TABLE tmp RENAME TO customers;
end;
$$;
COMMIT TRANSACTION;