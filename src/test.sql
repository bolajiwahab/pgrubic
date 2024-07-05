CREATE TABLE public.measurement (
    city_id         bigint not null,
    updated         text,
    created         timestamptz check (created > updated) not null,
    constraint measurement_city_id_updated_pkey primary key(city_id, updated)
)
;

-- CREATE or replace VIEW nums_1_100 (n) AS
--     -- with a as (select 1)
--     select * from a
-- UNION ALL
--     SELECT nums_1_102.n FROM public.nums_1_101 WHERE nums_1_102.n < 100;

-- update tbl set a = 20
-- ;

-- alter table tble set tablespace col;
