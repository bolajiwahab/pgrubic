-- CREATE DATABASE "Music2"
--     LOCALE 'sv_SE.iso885915'
--     ENCODING SQL_ASCII
--     TEMPLATE template0
-- ;

-- CREATE TABLE "measurement_y2006m02" PARTITION OF public.measurement
--     FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');


-- CREATE TYPE "mood" AS ENUM ('sad', 'ok', 'happy');

-- CREATE TRIGGER "Check_update"
--     BEFORE UPDATE ON accounts
--     FOR EACH ROW
--     EXECUTE FUNCTION check_account_update();

-- CREATE ROLE "Jonathan" LOGIN;

-- CREATE TABLESPACE "Dbspace" LOCATION '/data/dbs';

-- CREATE SEQUENCE "Serial" START 101;

-- CREATE RULE notify_me AS ON UPDATE TO mytable DO ALSO NOTIFY mytable -- noqa: COV003
-- ;
-- CREATE MATERIALIZED VIEW "Vista"
--   AS SELECT 'Hello World';

CREATE TABLE "_protectedaccounts" (MATERIALIZED timestamptz);

CREATE FUNCTION "add"(integer, integer) RETURNS integer
    AS 'select $1 + $2;'
    LANGUAGE SQL
    IMMUTABLE
    RETURNS NULL ON NULL INPUT;

-- CREATE FUNCTION public."Add"(
--                              -- CREATE TABLE public."Films_recent" AS
-- --   SELECT * FROM films WHERE date_prod >= '2002-01-01';
-- create index "Ab" on ba(a);
-- integer,
--                              integer)
-- RETURNS integer
-- AS $$select $1 + $2;$$
-- -- hello

-- LANGUAGE sql IMMUTABLE RETURNS NULL ON NULL INPUT;
-- create index abc on bac(ac) -- noqa: UNS001
-- ;
-- alter table tbl alter column "Az" set not null;
-- alter table tbl add column "Aa" text not null;

-- CREATE TABLE people (
--     height_cm numeric,
--     height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
-- );
-- ALTER TABLE employee
-- ADD CONSTRAINT "Employee_unq" primary key(email)
-- ;
-- CREATE TABLE distributors (
--     did     bigserial PRIMARY KEY,
--     -- cid     time with time zone,
--     -- diid    timestamptz,
--     biid    timestamp,
--     -- bid money
--     Name  "char" not null,
--     Name  varchar(40) not null
-- );
-- CREATE TABLE "measurement_y2006m02" () INHERITS (measurement);
/* 
                                                 hello 
                                                 */
-- ALTER TABLE public.ecdict ADD COLUMN id serial /* hello */ -- noqa: UNS019, UNS021
-- ;
/* 
                                                 hello 
                                                 */
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
-- VACUUM full analyze tbl;
-- cluster tbl;
-- ALTER TABLE measurement DETACH PARTITION measurement_y2006m02
-- ;
-- REFRESH MATERIALIZED VIEW tbl;
-- REINDEX TABLE CONCURRENTLY my_broken_table
-- ;
-- REINDEX INDEX my_broken_index;
-- REINDEX DATABASE CONCURRENTLY dba;
-- REINDEX SCHEMA CONCURRENTLY my_broken_schema;
