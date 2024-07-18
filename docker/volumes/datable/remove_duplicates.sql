BEGIN TRANSACTION;
do
$$
begin
    create TABLE tmp as with remove_duplicates as (
        SELECT *, LAG(event_time) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevTime,
        LAG(product_id) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevProduct,
        LAG(event_type) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevEvent_type,
        LAG(user_id) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevUser_id,
        LAG(user_session) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevUser_session,
        LAG(price) over (partition by event_type, product_id, price, user_id, user_session ORDER BY event_time) as prevPrice
        FROM customers)
    SELECT event_time, event_type, product_id, price, user_id, user_session
    FROM remove_duplicates
    where user_id != user_id or user_session != user_session or price != price or prevEvent_type != event_type or prevProduct != product_id or event_time - prevTime > INTERVAL '1 second' or prevTime IS NULL;

    DROP TABLE customers;
    alter TABLE tmp RENAME TO customers;
end;
$$;
COMMIT TRANSACTION;
