CREATE TABLE public."Color"();

-- ALTER TABLE public.incoming_credit
--     ADD COLUMN account_id UUID NOT NULL;

-- CREATE TABLE public.hello (
--     city_id         bigint not null,
--     updated         text,
--     updated         text,
--     created         timestamptz check (created > updated) not null,
--     hello           float,
--     constraint measurement_city_id_updated_pkey primary key(city_id, updated)
-- )
-- ;

-- CREATE or replace VIEW nums_1_100 (n) AS
--     -- with a as (select 1)
--     select * from a
-- UNION ALL
--     SELECT nums_1_102.n FROM public.nums_1_101 WHERE nums_1_102.n < 100;

-- CREATE TABLE color (
--     color_id INT GENERATED BY DEFAULT AS IDENTITY,
--     color_name VARCHAR NOT NULL
-- );


-- update public.tbl set a = 20 -- noqa: UNT010
-- ;

-- delete from public.tbl -- noqa: *
-- ;

-- select a = null;
-- alter table tble set tablespace col;
