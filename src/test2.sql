-- pgrubic: noqa
CREATE INDEX idx
    ON public.tbl (activated);

CREATE INDEX idx
    ON -- pgrubic: noqa
-- noqa: CVP
public.tbl (activated);

CREATE TABLE -- noqa: CVP003
public.tbl (
    activated date,
    CONSTRAINT activated_pkey PRIMARY KEY (activated)
);
