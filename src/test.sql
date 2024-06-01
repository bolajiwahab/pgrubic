-- CREATE DATABASE music2
--     LOCALE 'sv_SE.iso885915'
--     ENCODING SQL_ASCII
--     TEMPLATE template0
-- ;

-- CREATE RULE notify_me AS ON UPDATE TO mytable DO ALSO NOTIFY mytable -- noqa: COV003
-- ;

-- create index 
-- ab on ba(a);

-- create index abc on bac(ac) -- noqa: UNS001
-- ;

-- alter table tbl alter column a set not null;
-- alter table tbl add column a text not null;

-- CREATE TABLE people (
--     height_cm numeric,
--     height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
-- );

CREATE TABLE distributors (
    did     bigserial PRIMARY KEY,
    -- cid     time with time zone,
    -- diid    timestamptz,
    -- biid    timestamp(0),
    bid money
    -- Name  varchar(40) not null
);

-- CREATE TABLE "Measurement_y2006m02" () INHERITS (measurement);

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

-- ALTER TABLE public.ecdict ADD COLUMN id bigserial PRIMARY KEY;

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
