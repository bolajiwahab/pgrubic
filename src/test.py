import re

def find_sql_statements(sql_string):
    # Regular expression to match SQL statements ending with a semicolon
    pattern = re.compile(r'[^;]+;')
    
    statements = []
    for match in pattern.finditer(sql_string):
        statement = match.group().strip()
        start_index = match.start()
        end_index = match.end() - 1  # Adjust because end() is the position after the last character
        statements.append((statement, start_index, end_index))
    
    return statements

# Example usage:
sql_string = """
SELECT 1;
SELECT 10 -- noqa: hahaha;
;
SELECT a, b, c FROM table;
"""

statements = find_sql_statements(sql_string)
for stmt, start, end in statements:
    print(f"Statement: {stmt}, Start index: {start}, End index: {end}")
