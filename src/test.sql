-- select * from amex.tbl where b = null;

-- CREATE INDEX i0 ON t0((nullif(FALSE, 'NULL')));

-- select * from foo where col not in (1,null);

-- select null * a;

-- begin;
-- -- create index concurrently i0 on t0((nullif(FALSE, 'NULL')));
-- select * from amex.tbl where b = false;
-- end;

-- SELECT a = NULL;
-- create table foo (a integer null, b integer not null);

-- CREATE TYPE mood AS ENUM ('sad', 'ok', 'NULL');

-- ALTER TYPE public.phone_pairing_state ADD VALUE 'NULL';

-- create table amex.tbl(ay text default 'null');

-- select a = 'null';

-- select 'okay' = a;

-- select null = a;

-- select a = NULL;

create table amex.tbl(ay text null, created timestamptz, received timestamptz);

-- CREATE TABLE amex.tbl (
--     id text DEFAULT NULL
--   , created timestamptz
--   , updated_at timestamptz NOT NULL
-- );

-- alter table amex.tbl alter column ay type uuid using (id::uuid, user_id::uuid);

-- CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text)
--     AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
--     LANGUAGE SQL;
