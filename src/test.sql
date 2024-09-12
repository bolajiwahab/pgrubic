-- CREATE TYPE mood AS ENUM ('sad', 'ok', 'NULL');

-- ALTER TYPE phone_pairing_state ADD VALUE 'NULL';

-- CREATE TYPE public.final_status AS ENUM (
--     'AUTHENTICATED',
--     'CHALLENGED',
--     'EXEMPTED',
--     'FAILED',
--     'REJECTED',
--     'UNKNOWN'
-- );

-- create table tbl (age bigint, mood mood, phone_pairing_state phone_pairing_state, final_status final_status);

-- CREATE TABLE measurement_y2006m02 () INHERITS (measurement);

ALTER TABLE public.music DROP COLUMN created, DROP COLUMN created; ALTER TABLE public.music DROP COLUMN created;

-- CREATE TABLE public.secure_transaction (
--     partition_date               date                     NOT NULL,
--     id                           uuid                     NOT NULL,
--     created                      timestamp with time zone NOT NULL,
--     updated                      timestamp with time zone NOT NULL,
--     card_id                      uuid                     NOT NULL,
--     decision_reason              text                             ,
--     notified                     timestamp with time zone         ,
--     risk_model_decision          public.risk_model_decision       ,
--     risk_model_version           text                             ,
--     status                       public.status            NOT NULL,
--     user_id                      uuid                     NOT NULL,
--     authentication_id            uuid                             ,
--     external_transaction_id      uuid                             ,
--     acs_transaction_id           uuid                             ,
--     final_status                 public.final_status              ,
--     final_status_reason          text                             ,
--     external_ecommerce_indicator text                             ,
--     exemption_identifier         text                             ,

--     CONSTRAINT secure_transaction_pkey
--         PRIMARY KEY (id, partition_date),

--     CONSTRAINT secure_transaction_acs_transaction_id_key
--         UNIQUE (acs_transaction_id, partition_date)
-- ) PARTITION BY RANGE (partition_date);

-- CREATE DATABASE music ENCODING "sql_ascii" TEMPLATE template0;
