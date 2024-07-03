-- select;
ALTER TABLE public.ecdict ADD COLUMN id bigint default now() not null -- noqa: USR002
;

/*
sel
ect;
*/

-- select;

ALTER TABLE public.ecdict
ADD COLUMN id bigint default current_timestamp not null -- select 1 -- noqa: USR002
;

-- -- create table ecdict()
-- ALTER TABLE public.ecdict alter deleted drop not null /* hello */ -- noqa: UNS021, UNS019
-- 

-- REINDEX SCHEMA CONCURRENTLY my_broken_schema

ALTER TABLE public.ecdict ADD COLUMN id bigint default current_timestamp not null -- noqa: USR002
;

-- REINDEX SCHEMA CONCURRENTLY my_broken_schema;
