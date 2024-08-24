-- select * from amex.tbl where b = null;

-- CREATE INDEX i0 ON t0((nullif(FALSE, 'NULL')));

select * from foo where col not in (1,null);

-- select null * a;

-- begin;
-- -- create index concurrently i0 on t0((nullif(FALSE, 'NULL')));
-- select * from amex.tbl where b = false;
-- end;

-- SELECT a = NULL;

-- ALTER TYPE public.phone_pairing_state ADD VALUE 'NULL';

-- create table amex.tbl(ay text default 'null');

-- alter table amex.tbl alter column ay type uuid using (id::uuid, user_id::uuid);
