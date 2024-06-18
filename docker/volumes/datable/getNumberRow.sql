do 
$$
declare
    t_name text;
	n int;
begin
    create TEMP TABLE tmp (name text, numberrow int);
	FOR t_name in SELECT unnest(enum_range(NULL::eventtype)) loop
		n := count(event_type) FROM public.customer where event_type = t_name::eventtype;
		insert into tmp (name, numberrow) values (t_name, n);
	end loop;
end; 
$$;

select * from tmp;