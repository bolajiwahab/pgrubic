CREATE TYPE mood AS ENUM ('sad', 'ok', 'NULL');

ALTER TYPE phone_pairing_state ADD VALUE 'NULL';

CREATE TYPE public.final_status AS ENUM (
    'AUTHENTICATED',
    'CHALLENGED',
    'EXEMPTED',
    'FAILED',
    'REJECTED',
    'UNKNOWN'
);
