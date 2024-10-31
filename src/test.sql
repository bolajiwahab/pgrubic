-- -- ALTER TABLE public.example
-- --     ADD COLUMN foo boolean DEFAULT FALSE;
-- CREATE INDEX idx
--     ON public.tbl (activated);
-- CREATE TYPE test.mood AS ENUM (
--     'sad'
--   , 'ok'
-- );
SELECT a,
       b,
       c
  FROM tab;

-- -- ALTER TABLE music ADD COLUMN created_at timestamptz;
-- INSERT INTO public.music (date, created_at, date)
-- VALUES (now(), now(), now())
--      , (now(), now(), now())
--      , (now(), now(), now());
-- SELECT DISTINCT
--        col1
--   FROM test
--  ORDER BY col1;
-- SELECT DISTINCT
--        col1
--      , col2
--      , col3
--   FROM test
--  ORDER BY 1;
-- SELECT DISTINCT ON (col1)
--        col1
--      , col2
--      , col3
--   FROM test
--  ORDER BY col1;
-- -- update music
-- -- set created_at = now(), date = now()
-- -- where id = 1;
-- UPDATE p
--    SET p.listprice = p.listprice * 1.05
--      , p.modifieddate = getutcdate()
--   FROM production.product AS p
--  WHERE (p.sellenddate IS NULL
--    AND p.sellstartdate IS NOT NULL)
--     OR p.sellenddate IS NOT NULL;
-- SELECT p.name AS productname
--      , p.productnumber
--      , pm.name AS productmodelname
--      , p.color
--      , p.listprice
--   FROM production.product AS p
--  INNER JOIN production.productmodel AS pm
--     ON p.productmodelid = pm.productmodelid
--  WHERE p.color IN ('Blue', 'Red')
--    AND p.listprice < 800.00
--    AND pm.name LIKE '%frame%'
--  ORDER BY p.name;
-- SELECT *
--   INTO public.films_recent
--   FROM films
--  WHERE date_prod >= '2002-01-01';
-- CREATE TABLE films_recent AS
-- SELECT *
--   FROM films
--  WHERE created_at >= '2002-01-01';
-- SELECT *
--   FROM users
--  WHERE id = 1
--  UNION
-- SELECT *
--   FROM users
--  WHERE id = 2;
-- INSERT INTO public.films (title, description)
-- VALUES ('Pulp Fiction', 'Quentin Tarantino')
--     ON CONFLICT (title)
--     DO NOTHING
--     RETURNING *;
-- INSERT INTO distributors (did, dname)
-- VALUES (5, 'Gizmo Transglobal')
--      , (6, 'Associated Computing, Inc')
--     ON CONFLICT (did)
--     DO UPDATE SET dname = excluded.dname
--                 , did = excluded.did;
-- INSERT INTO distributors (did, dname)
-- VALUES (10, 'Conrad International')
--     ON CONFLICT (did) WHERE is_active
--     DO NOTHING;
-- CREATE UNIQUE INDEX CONCURRENTLY IF NOT EXISTS savings_account_core_account_id_key
--     ON public.savings_account (core_account_id, account_type);
-- UPDATE interest_rate_policy
--    SET applied = NULL
--  WHERE name = 'RoEBusinessMembershipTieredIRAug2024'
--     OR name = 'RoEMembershipTieredIRAug2024'
--     OR name = 'SpainMembershipTieredIRAug2024'
--     OR name = 'FranceMembershipTieredIRAug2024'
--     OR name = 'GermanyMembershipTieredIRAug2024';
-- ALTER TABLE public.savings_account
--     ADD CONSTRAINT unique_core_account_id UNIQUE USING INDEX savings_account_core_account_id_key;
-- ALTER TABLE distributors
--     DROP CONSTRAINT distributors_pkey
--   , ADD CONSTRAINT distributors_pkey PRIMARY KEY USING INDEX dist_id_temp_idx;
-- INSERT INTO public.films (title, description)
-- VALUES ('Pulp Fiction', 'Quentin Tarantino')
--     ON CONFLICT (title, description) WHERE title = 'Pulp Fiction'
--     DO NOTHING
--     RETURNING *;
-- INSERT INTO public.films (title, description)
-- VALUES ('Pulp Fiction', 'Quentin Tarantino')
--     ON CONFLICT
--     DO NOTHING
--     RETURNING *;
--     WITH films AS (
--         INSERT INTO public.films (title, description) VALUES
--         ('Pulp Fiction', 'Quentin Tarantino')
--         RETURNING *
--     )
--     SELECT * FROM public.films;
WITH films AS (
    INSERT INTO public.films (title, description)
    VALUES ('Pulp Fiction', 'Quentin Tarantino')
    RETURNING *
)
, films2 AS (
    SELECT *
      FROM public.films
)
, films3 AS (
    SELECT *
      FROM public.films
)
INSERT INTO public.films (title, description)
VALUES ('Pulp Fiction', 'Quentin Tarantino')
RETURNING *;

WITH films AS (
    SELECT *
      FROM public.films
)
INSERT INTO public.films (title, description)
VALUES ('Pulp Fiction', 'Quentin Tarantino')
RETURNING *;

SELECT a
      , b
      , c
  FROM films
  WHERE date_prod >= '2002-01-01'
    OR id = 2
    AND id = 3
  ORDER BY date_prod DESC
  LIMIT 100
OFFSET 5;
