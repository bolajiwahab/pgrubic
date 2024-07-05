sql_code = """
CREATE or replace VIEW nums_1_100 (n) AS
    -- with a as (select 1)
    SELECT * FROM a
UNION ALL
    SELECT nums_1_102.n FROM public.nums_1_101 WHERE nums_1_102.n < 100;
"""

# Define the total width for alignment
width = 80

# Center-align each line
center_aligned_code = "\n".join(line.rjust(50) for line in sql_code.strip().split('\n'))

print(center_aligned_code)
