create type EventType as enum (
    'view',
    'cart',
    'remove_from_cart',
    'purchase'
);

BEGIN TRANSACTION;

do 
$$
declare
    me text;
    count int;
begin
    SET client_min_messages TO WARNING;
    DROP TABLE IF EXISTS files;
    CREATE TEMP TABLE files(ame text);
    execute FORMAT($cmd$ COPY files FROM PROGRAM 'find %s -maxdepth 1 -type f -printf "%%f\n"' $cmd$, '/tmp');
    for me in SELECT ame FROM files loop
        execute FORMAT($cmd$ create TABLE %s (event_time timestamptz, event_type EventType, product_id int, price float, user_id int8, user_session varchar(255)) $cmd$, substring (me from 1 FOR strpos(me, '.') -1 ));
        execute FORMAT($cmd$ COPY %s (event_time, event_type, product_id, price, user_id, user_session) FROM '/tmp/%s' DELIMITER ',' CSV HEADER; $cmd$, substring (me from 1 FOR strpos(me, '.') -1 ), me);
    end loop;
    
end; 
$$;

COMMIT TRANSACTION;