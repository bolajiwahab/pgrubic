-- create index 
-- ab on ba(a);
-- create index abc on bac(ac);

-- alter table tbl alter column a set not null;
-- alter table tbl add column a text not null;

-- CREATE TABLE people (
--     height_cm numeric,
--     height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
-- );

/* 
hello 
*/
ALTER TABLE public.ecdict ADD COLUMN id serial /* hello */ -- noqa: UNS019, UNS021
;
/* 
hello 
*/
ALTER TABLE public.ecdict ADD COLUMN id serial /* hello */ -- noqa: UNS021
;
/* hello */
ALTER TABLE public.ecdict ADD COLUMN id bigint GENERATED ALWAYS AS IDENTITY -- noqa: UNS020
;

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

-- cluster;

-- REFRESH MATERIALIZED VIEW tbl;

-- REINDEX TABLE my_broken_table;

-- REINDEX INDEX my_broken_index;

-- REINDEX DATABASE CONCURRENTLY dba;

-- REINDEX SCHEMA CONCURRENTLY my_broken_schema;
