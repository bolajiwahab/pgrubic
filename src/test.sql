select current_time -- noqa: GN020
;

create table public.ecdict (id bigserial);

-- ALTER TABLE public.ecdict alter COLUMN id type bigserial -- noqa: TYP009;
ALTER TABLE public.card ADD CONSTRAINT fkey FOREIGN KEY (account_id) REFERENCES public.account (id)
