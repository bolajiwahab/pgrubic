CREATE TABLE IF NOT EXISTS public.theoretical_allowance (
    year_month              date                        NOT NULL,
    account_id              uuid                        NOT NULL,
    allowance               numeric                     NOT NULL,
    adjustment              numeric                     NOT NULL,
    created                 timestamp with time zone    NOT NULL,
    updated                 timestamp with time zone    NOT NULL,

    CONSTRAINT allowance_pkey PRIMARY KEY (account_id, year_month),
    CONSTRAINT allowance_year_month_format_check CHECK (EXTRACT(DAY FROM year_month) = 1)
);

CREATE TRIGGER trigger_allowance_set_dates
    BEFORE INSERT OR UPDATE
    ON public.theoretical_allowance
    FOR EACH ROW EXECUTE PROCEDURE set_dates();
