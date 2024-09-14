-- SELECT a, b, c FROM d
-- where f = 10 and g = 20 and c > 0 and d > 10 and b < 5 -- or a = 1
-- order by c
-- fetch next 10 row only
-- FOR UPDATE;

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

CREATE INDEX ON measurement (logdate, city_id);
