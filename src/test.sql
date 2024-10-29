-- ALTER TABLE public.example
--     ADD COLUMN foo boolean DEFAULT FALSE;

CREATE INDEX idx
    ON public.tbl (activated);

CREATE TYPE test.mood AS ENUM ('sad', 'ok');

SELECT a
     , b
     , c
  FROM tab;

-- ALTER TABLE music ADD COLUMN created_at timestamptz;

INSERT INTO public.music (date, created_at, date)
VALUES (now(), now(), now()), (now(), now(), now()), (now(), now(), now());

select distinct(col1) from test order by col1;
select distinct col1,col2,col3 from test order by 1;
select distinct on (col1) col1,col2,col3 from test order by col1;
-- update music
-- set created_at = now(), date = now()
-- where id = 1;

update p
   set p.ListPrice = p.ListPrice * 1.05
     , p.ModifiedDate = getutcdate()
  from Production.Product as p
 where p.SellEndDate is null
   and p.SellStartDate is not null or p.SellEndDate is not null;


select p.Name as ProductName
     , p.ProductNumber
     , pm.Name as ProductModelName
     , p.Color
     , p.ListPrice
  from Production.Product as p
  join Production.ProductModel as pm
    on p.ProductModelID = pm.ProductModelID
 where p.Color in ('Blue', 'Red')
   and p.ListPrice < 800.00
   and pm.Name like '%frame%'
 order by p.Name
;

SELECT *
    INTO public.films_recent
    FROM films
    WHERE date_prod >= '2002-01-01';

CREATE TABLE films_recent AS
SELECT *
  FROM films
 WHERE created_at >= '2002-01-01';
