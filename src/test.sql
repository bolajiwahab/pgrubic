select -- noqa: GN020
current_time 
;

vacuum full public.ecdict;

REFRESH MATERIALIZED VIEW order_summary;

select current_time -- noqa: NM009
;

-- select ; CURRENT_TIME;

-- CREATE DATABASE music
--     ENCODING SQL_ASCII
--     TEMPLATE template0;

-- ALTER TABLE child_table 
-- ADD CONSTRAINT constraint_name 
-- FOREIGN KEY (fk_columns) -- noqa: UN015, GN020,   GN020
-- REFERENCES parent_table (parent_key_columns) on update cascade on delete cascade;

-- CREATE TABLE films_recent AS SELECT * FROM films WHERE date_prod >= '2002-01-01';

-- drop table tab cascade;

-- SELECT * INTO films_recent FROM films WHERE date_prod >= '2002-01-01';
-- SELECT * INTO films_recent2 FROM films2 WHERE date_prod >= '2002-01-01';

-- REINDEX database my_index;

-- ALTER table percona.foo_id_idx SET TABLESPACE newtblspc;

-- ALTER TABLE public.ecdict ADD COLUMN ecdict_id bigint not null default current_time;

-- ALTER TABLE public.ecdict1 alter COLUMN ecdict_id type serial;

-- ALTER TABLE products ALTER COLUMN product_no SET NOT NULL

-- ALTER TABLE public.ecdict1 alter product_no set not null;

-- CREATE TABLE amlex.f (i text) -- noqa: NM014, GN004
-- ;

-- CREATE TABLE amlex.foo (bar text) -- noqa: NM014, GN004
-- ;

-- alter table tab add column account_id numeric;

-- create table tab2 (
--     id numeric
-- );

-- CREATE TABLE people (
--     id numeric,
--     height_cm numeric,
--     height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
-- );

-- create table tbl(
--     age int null
-- );
