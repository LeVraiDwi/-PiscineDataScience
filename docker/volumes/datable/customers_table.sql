BEGIN TRANSACTION;
do 
$$
declare
    t_name text;
begin
    create TEMP TABLE tmp (table_name text);
    insert into tmp (table_name) SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' and table_name like 'data_202_\____';
    create TABLE customer (event_time timestamptz, event_type EventType, product_id int, price float, user_id int8, user_session varchar(255));
    for t_name in SELECT table_name FROM tmp loop
        execute FORMAT($cmd$ insert into customer (event_time, event_type, product_id, price, user_id, user_session) SELECT * FROM %s $cmd$, t_name);
    end loop;
end; 
$$;
COMMIT TRANSACTION;