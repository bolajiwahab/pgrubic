create index idx
  on production.product (listprice);

-- fmt: skip
create index idx2
  on production.product (listprice);

TRUNCATE TABLE public.card;
TRUNCATE TABLE public.card;

-- The prefix semicolon is clear and easy to spot when adding to a `where`
WITH a AS (
    SELECT *
      FROM production.product
)
, age AS (
    SELECT *
      FROM production.product
)
update a
   SET listprice = age.listprice
  FROM age
 WHERE a.listprice = age.listprice;

-- This is a comment
-- This is also a comment
select
       a
      , b
      , c
  FROM tab;
