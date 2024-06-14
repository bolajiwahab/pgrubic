CREATE TABLE measurement (
    city_id         bigint not null,
    updated         timestamptz,
    created         timestamptz,
    constraint measurement_city_id_updated_key unique(city_id, updated)
)
;

ALTER TABLE public.ecdict alter deleted drop not null /* hello */ -- noqa: UNS021, UNS019
;


-- select created, updated from tbl;
-- CREATE TABLE partitions."public__measurement__y2006m02" PARTITION OF public.measurement
--     FOR VALUES FROM ('2006-02-01 00:00:00+00') TO ('2006-02-28 00:00:00+00') -- noqa: CVP001
-- ;

-- create extension postgis with schema "Public1";

-- CREATE SEQUENCE public.serial_seq START 101;

-- CREATE TYPE uyt."pg_add" AS ENUM ('sad', 'ok', 'happy');

-- CREATE TRIGGER "Check_update"
--     BEFORE UPDATE ON accounts
--     FOR EACH ROW
--     EXECUTE FUNCTION check_account_update();

-- CREATE ROLE "Jonathan" LOGIN;

-- CREATE TABLESPACE "Dbspace" LOCATION '/data/dbs';

-- CREATE SEQUENCE "Serial" START 101;

-- CREATE RULE notify_me AS ON UPDATE TO mytable DO ALSO NOTIFY mytable -- noqa: COV003
-- ;
-- drop schema public -- noqa: UNS003
-- ;
-- CREATE VIEW public."vista"
--   AS SELECT 'Hello World';

-- CREATE TABLE "_protectedaccounts" (MATERIALIZED timestamptz);

-- CREATE FUNCTION public."add"(integer, integer) RETURNS integer
--     AS 'select $1 + $2;'
--     LANGUAGE SQL
--     IMMUTABLE
--     RETURNS NULL ON NULL INPUT;

-- -- CREATE FUNCTION public."Add"(
-- --                              -- CREATE TABLE public."Films_recent" AS
-- -- --   SELECT * FROM films WHERE date_prod >= '2002-01-01';
-- create index "Abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzaazyuauauaip" on da(a, b, c)
-- ;

-- -- integer,
-- --                              integer)
-- -- RETURNS integer
-- -- AS $$select $1 + $2;$$
-- -- -- hello

-- -- LANGUAGE sql IMMUTABLE RETURNS NULL ON NULL INPUT;
-- -- create index abc on bac(ac) -- noqa: UNS001
-- -- ;
-- alter table tbl alter column "Az" set not null;
-- alter table tbl add column "Aa" text not null;

-- truncate table test;

-- CREATE TABLE people (
--     id SMALLINT,
--     height_cm jsonb,
--     height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
-- );

-- ALTER TABLE employee
-- ADD CONSTRAINT "employee_chk" check(length(email) = 60)
-- ;

-- CREATE TABLE distributors (
--     did     smallserial PRIMARY KEY,
--     -- cid     time with time zone,
--     -- diid    timestamptz,
--     biid    timestamp,
--     -- bid money
--     Name  "char" not null,
--     Name  varchar(40) not null
-- );
-- CREATE TABLE "measurement_y2006m02" (a int) INHERITS (measurement)
-- ;
-- /* 
--                                                  hello 
--                                                  */
-- ALTER TABLE public.ecdict ADD COLUMN id serial /* hello */ -- noqa: UNS019, UNS021
-- ;
-- /* 
--                                                  hello 
--                                                  */
-- create index abc on bac(ac)
-- ;
-- ALTER TABLE public.ecdict ADD COLUMN id serial /* hello */ -- noqa: UNS021, UNS019
-- ;
-- /* hello */
-- ALTER TABLE public.ecdict ADD COLUMN id bigint GENERATED ALWAYS AS IDENTITY -- noqa: UNS020
-- ;
-- ALTER TABLE transaction ADD COLUMN "transactionDate" timestamp without time zone GENERATED ALWAYS AS ("dateTime"::date) STORED;
-- alter table tbl drop column a;
-- alter table abc add constraint fkey foreign key(a) references bc(a);
-- alter table abc add constraint uniq unique using index tbl;
-- alter table abc add constraint uniq primary key using index tbl;
-- alter index all in tablespace tble set tablespace col;
-- alter table all in tablespace tble set tablespace col;
-- alter index tble set tablespace col;
-- alter table tble set tablespace col;
-- alter table tbl rename column b to c;
-- ALTER TABLE public.ecdict ADD COLUMN id bigserial PRIMARY KEY not null;
-- alter table tbl1 rename to tbl3;
-- alter table tble alter column set type text;
-- VACUUM FULL analyze tbl;
-- cluster tbl;
-- ALTER TABLE measurement DETACH PARTITION measurement_y2006m02
-- ;
-- REFRESH MATERIALIZED VIEW tbl;
-- REINDEX TABLE CONCURRENTLY my_broken_table
-- ;
-- REINDEX INDEX my_broken_index;
-- REINDEX DATABASE CONCURRENTLY dba;
-- REINDEX SCHEMA CONCURRENTLY my_broken_schema;
