-- select current_time -- noqa: GN020
-- ;

-- create table public.ecdict (id bigserial);

-- -- ALTER TABLE public.ecdict alter COLUMN id type bigserial -- noqa: TYP009;
-- ALTER TABLE card ADD CONSTRAINT fkey FOREIGN KEY (account_id) REFERENCES public.account (id);

-- CREATE MATERIALIZED VIEW public.mymatview AS SELECT * FROM public.mytab;

-- CREATE RECURSIVE VIEW amex.nums_1_100 (n) AS
--     VALUES (1)
-- UNION ALL
--     SELECT n+1 FROM amex.nums_1_100 WHERE n < 100;

WITH RECURSIVE included_parts(sub_part, part) AS (
    SELECT sub_part, part FROM amex.parts WHERE part = 'our_product'
  UNION ALL
    SELECT p.sub_part, p.part
    FROM amex.included_parts pr, parts p
    WHERE p.part = pr.sub_part
)
DELETE FROM amex.parts
  WHERE part IN (SELECT part FROM included_parts);
