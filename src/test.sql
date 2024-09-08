-- SELECT a = 'NULL';
-- select 'null';
-- create table foo (a integer null, b integer not null);

-- CREATE TYPE mood AS ENUM ('sad', 'ok', 'NULL');

-- ALTER TYPE phone_pairing_state ADD VALUE 'NULL';

drop procedure mood;
-- ALTER FUNCTION check_password(text) SET search_path = admin, pg_temp;

-- alter function public.mood set search_path = public;
-- alter table public.mood set schema public;
drop table mood, public.test;
-- create table amex.tbl(ay text default 'null');

-- select a = 'null';

-- select null != a;

-- select 'okay' = b;
-- select null = a;

-- select NULL = 'okay';

-- create table amex.tbl(ay text null, created timestamptz, received timestamptz);

-- CREATE TABLE amex.tbl (
--     id text DEFAULT NULL
--   , created timestamptz
--   , updated_at timestamptz NOT NULL
-- );

-- alter table amex.tbl alter column ay type uuid using (id::uuid, user_id::uuid);

CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text)
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    LANGUAGE SQL;
-- noqa: UN020
-- reindex table tbl -- okay
-- ;

-- ALTER TABLE public.card ADD CONSTRAINT chk CHECK (account_id > 0);
