-- CREATE PROCEDURE insert_data(a integer, b integer)
-- LANGUAGE SQL
-- AS $$
-- INSERT INTO tbl VALUES (a);
-- INSERT INTO tbl VALUES (b);
-- $$;

-- select a <> null;
-- create table public.bay as select * from ayaya;

CREATE TABLE yamaya.measurement_y2006m02 PARTITION OF yamaya.measurement
    FOR VALUES FROM ('2006-02-01 00:00:00') TO ('2006-03-02');

-- CREATE TABLE people (
--     "ID" numeric,
--     height_in numeric GENERATED ALWAYS AS (2/2.54) STORED
-- );
-- drop table aj, cj cascade;
-- create MATERIALIZED VIEW public.bay as select * from public.ayaya;
-- with a as (select * from public.ayaya)
-- SELECT * INTO films_recent FROM films WHERE date_prod >= '2002-01-01';
-- drop index CONCURRENTLY public.ayaya cascade;
-- select * from public.ade;
-- alter table public.car alter column name drop not null;
--- jello
-- CREATE TABLE public.color_id(
--     color_id bigint,
--     color_id bigint,
--     created bigint

-- ) -- noqa:
-- ;

-- drop index ayaya;
-- CREATE TYPE public.address_type AS(
--    street text, 
--    city text,
--    state text, 
--    country text
-- );

-- CREATE TYPE mood AS ENUM ('sad', 'ok', 'happy');

-- create view ayaya as select 1;

-- ALTER INDEX public.ayaya RENAME TO new_name

-- CREATE TABLE public.color(
--     color_id point primary key,
--     created boolean

-- ) -- noqa:
-- ;

-- alter table temp.color_id add column created serial;

-- CREATE RECURSIVE VIEW public.nums_1_100 (n) AS
--     VALUES (1)
-- UNION ALL
--     SELECT n+1 FROM nums_1_100 WHERE n < 100;

-- alter table temp.color_id add column color_id timestamptz, add column color_id timestamptz;
-- SELECT * INTO films_recent FROM films WHERE date_prod >= '2002-01-01';

-- select b = true from b where c = 10 -- noqa: MIS002, CVS001
-- ;

-- CREATE LANGUAGE plpython3u;

-- create extension pg_buffercache
-- ;

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

-- delete from public.tbl -- noqa: UNT010
-- ;

-- select a = null;
-- alter table tble set tablespace col;

-- select b = true from b where c = 10 -- noqa: MIS003
-- ;
