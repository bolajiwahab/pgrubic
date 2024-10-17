SELECT * FROM my_table; SELECT * FROM our_table; INSERT INTO -- this is a comment
my_table VALUES (1, 'example');

-- CREATE PROCEDURE insert_data(a integer, b integer)
-- LANGUAGE SQL
-- AS $$
-- INSERT INTO tbl VALUES (a);
-- INSERT INTO tbl VALUES (b);
-- $$;

-- CREATE MATERIALIZED VIEW amex.rental_by_category
-- AS
--  SELECT c.name AS category,
--     sum(p.amount) AS total_sales
--    FROM (((((payment p
--      JOIN rental r ON ((p.rental_id = r.rental_id)))
--      JOIN inventory i ON ((r.inventory_id = i.inventory_id)))
--      JOIN film f ON ((i.film_id = f.film_id)))
--      JOIN film_category fc ON ((f.film_id = fc.film_id)))
--      JOIN category c ON ((fc.category_id = c.category_id)))
--   GROUP BY c.name
--   ORDER BY sum(p.amount) DESC
-- WITH NO DATA;

-- CREATE RECURSIVE VIEW amex.pg_nums_1_100 (n) AS
--     VALUES (1)
-- UNION ALL
--     SELECT n+1 FROM nums_1_100 WHERE n < 100;
-- CREATE TYPE "pg_Compfoo" AS (f1 bigint, f2 text);

ALTER TABLE child_table
ADD CONSTRAINT constraint_name
FOREIGN KEY (fk_columns)
REFERENCES parent_table (parent_key_columns);

-- select a <> null;
-- create table "Bay" as select * from ayaya;

-- SELECT * INTO Films_recent FROM films WHERE date_prod >= '2002-01-01';

-- CREATE TABLE yamaya.measurement_y2006m02 PARTITION OF yamaya.measurement
--     FOR VALUES FROM ('2006-03;-01') TO ('2006-03-07 23:59:59.999');
-- select 1;

select 1
;
