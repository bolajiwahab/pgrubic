CREATE TABLE IF NOT EXISTS public.monthly_calculation_result (
    calculation_month date NOT NULL
  , account_id uuid NOT NULL
  , year_month date NOT NULL
  , created timestamp with time zone NOT NULL
  , updated timestamp with time zone NOT NULL
  , triggered_at timestamp with time zone NOT NULL
  , incoming numeric NOT NULL
  , spending numeric NOT NULL
  , raw_allowance numeric NOT NULL
  , income_allowance numeric NOT NULL
  , activated_allowance numeric NOT NULL
  , income_payout numeric NOT NULL
  , carryover numeric NOT NULL
  , carryover_payout numeric NOT NULL
  , balance numeric NOT NULL
  , carryover_bundle jsonb
  , overlap_spending numeric
  , limit_adjustment numeric
  , creditor_payout numeric
  , dd_dr_adjustment numeric
  , CONSTRAINT monthly_calculation_result_pkey PRIMARY KEY (account_id, year_month, calculation_month)
  , CONSTRAINT monthly_calculation_result_calculation_month_format_check CHECK (EXTRACT(DAY FROM calculation_month) = 1)
  , CONSTRAINT monthly_calculation_result_year_month_format_check CHECK (EXTRACT(DAY FROM year_month) = 1)
)
PARTITION BY RANGE (calculation_month);
