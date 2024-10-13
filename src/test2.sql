-- pgrubic: noqa
CREATE INDEX idx
    ON -- noqa: COV011
public.tbl (activated);

CREATE TABLE public.tbl (
    activated date,
    CONSTRAINT activated_pkey PRIMARY KEY (activated)
);
