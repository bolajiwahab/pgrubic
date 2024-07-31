select current_time -- noqa: GN020, GN020,
;

select current_time -- noqa: NM009
;

-- select CURRENT_TIME;

ALTER TABLE child_table 
ADD CONSTRAINT constraint_name 
FOREIGN KEY (fk_columns) -- noqa: UN015, GN020,   GN020
REFERENCES parent_table (parent_key_columns);
