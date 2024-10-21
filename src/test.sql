ALTER TABLE public.example
    ADD COLUMN foo boolean DEFAULT FALSE;

CREATE INDEX idx
    ON public.tbl (activated);

CREATE TYPE test.mood AS ENUM ('sad', 'ok');

SELECT a
     , b
     , c
  FROM tab;

ALTER TABLE music ADD COLUMN created_at timestamptz;
