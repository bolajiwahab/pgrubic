-- SELECT a, b, c FROM d
-- where f = 10 and g = 20 and c > 0 and d > 10 and b < 5  -- or a = 1
-- order by c
-- fetch next 10 row only
-- FOR UPDATE;

-- select a, b, c from tbl where tbl.d = 10 or tbl.d = 12 or d = 30;

-- CREATE LANGUAGE plsample
--     HANDLER plsample_call_handler;

-- select 1;
-- ALTER TABLE tbl ADD CONSTRAINT tbl_exclusion EXCLUDE USING gist (tbl_id WITH &&);

-- ALTER TABLE tbl ADD CONSTRAINT tbl_exclusion EXCLUDE USING gist (tbl_id WITH &&);

-- CREATE TABLESPACE "TABLESPACE" LOCATION 'directory_path';

SELECT INTO tb$l FROM tbl;

-- CREATE INDEX "INDEX" ON tbl (col);

-- CREATE SEQUENCE "TABLE" START 1;

-- select a, b, c from tbl where tbl.d in(10 , 12, 30);


-- drop table test;

-- drop type public.typ cascade;

-- drop procedure func cascade;

-- alter table tbl drop column age cascade, drop column name cascade;

-- drop index idx_tbl_age cascade;

-- ALTER TABLE public.foos SET WITHOUT CLUSTER;

-- ALTER TABLE public.test ALTER COLUMN b DROP expression cascade;

-- drop schema test CASCADE;

-- CREATE TABLE people (
--     height_cm numeric,
--     height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
-- );

-- ALTER TABLE music ADD COLUMN created_at timestamp;

-- ALTER TABLE music ADD COLUMN created_at timestamp, ADD COLUMN updated_at timestamp;

-- CREATE INDEX ON measurement1 (logdate, city_id);

-- CREATE INDEX IF NOT EXISTS account_expr_idx1
--     ON public.account USING btree
--     ((some_data ->> 'user_id'), (some_data ->> 'user_id'))
--     WHERE (some_data ->> 'user_id') IS NULL;

-- CREATE UNIQUE INDEX if not exists emails_idx
-- ON account(user_id)
-- INCLUDE(id,id_old)
-- WHERE (some_data ->> 'user_id') IS NULL;

-- CREATE TYPE public.final_status AS ENUM (
--     'AUTHENTICATED',
--     'CHALLENGED',
--     'EXEMPTED',
--     'FAILED',
--     'REJECTED',
--     'UNKNOWN'
-- );

-- ALTER TYPE enum_type ADD VALUE  'new_value';

-- ALTER TYPE enum_type
--     ADD VALUE IF NOT EXISTS 'new_value';

-- ALTER TYPE enum_type ADD VALUE 'new_value' BEFORE 'old_value';
-- ALTER TYPE enum_type ADD VALUE 'new_value' AFTER 'old_value';

-- CREATE TABLE measurement_y2006m02 PARTITION OF measurement
--     FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');

-- CREATE TABLE measurement (
--     city_id         int not null,
--     logdate         date not null,
--     peaktemp        int,
--     unitsales       int
-- ) PARTITION BY RANGE (logdate)
-- tablespace ts_pgrubic;

-- CREATE TABLE measurement_y2006m02 () INHERITS (measurement);

-- CREATE unlogged TABLE distributors (
--     did     integer,
--     name    varchar(40),
--     UNIQUE(name) WITH (fillfactor=70)
-- )
-- WITH (fillfactor=70);

-- create temporary table tbl as select a, b, c from tbl;

-- CREATE TABLE partitions.public__outgoing_sms__2019_11
--     PARTITION OF public.outgoing_sms
--     FOR VALUES FROM ('2019-11-01 00:00:00+00') TO ('2019-12-01 00:00:00+00');

-- ALTER TABLE music ADD COLUMN created_at timestamp(0);
