-- pgrubic: noqa

CREATE INDEX idx on public.tbl(activated);

CREATE TABLE public.tbl (activated date, constraint activated_pkey primary key (activated));
