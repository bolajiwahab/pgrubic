select CURRENT_TIME;

-- ALTER TABLE child_table 
-- ADD CONSTRAINT constraint_name 
-- FOREIGN KEY (fk_columns) -- noqa: NM004
-- REFERENCES parent_table (parent_key_columns) not valid;


-- CREATE TABLE contacts(
--    contact_id INT GENERATED ALWAYS AS IDENTITY,
--    customer_id INT,
--    contact_name VARCHAR(255) NOT NULL,
--    phone VARCHAR(15),
--    email VARCHAR(100),
--    PRIMARY KEY(contact_id),
--    CONSTRAINT fk_customer
--       FOREIGN KEY(customer_id) 
--         REFERENCES customers(customer_id)
-- );

-- select a = null;
-- CREATE TABLE measurement_y2008m02 PARTITION OF measurement
--     FOR VALUES FROM ('2008-02-01') TO ('2008-03-01')
--     TABLESPACE fasttablespace;

-- ALTER TABLE mytable SET UNLOGGED; -- cheap!

-- CREATE UNLOGGED TABLE amlex.unlogged_table(test bigint, created timestamp with time zone not null,
-- updated timestamp with time zone not null, constraint unlogged_table_pkey PRIMARY KEY(test));

-- CREATE INDEX i0 ON t0((nullif(NULL, TRUE)));

-- get all foreign keys and indexes from __init__.py
-- then subclass and do our main check
-- propably have it in the same folder (two classes)
