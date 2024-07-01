import re

def replace_comments_with_spaces(sql):
    # Regex pattern for single-line comments at the start of a line
    single_line_pattern = re.compile(r'^--.*$', re.MULTILINE)
    # Regex pattern for multi-line comments at the start of a line
    multi_line_pattern = re.compile(r'^\s*/\*[\s\S]*?\*/\s*$', re.MULTILINE)

    # Function to replace matches with spaces of the same length
    def replace_with_spaces(match):
        return ' ' * len(match.group(0))
    
    # Replace single-line comments with spaces
    sql = single_line_pattern.sub(replace_with_spaces, sql)
    # Replace multi-line comments with spaces
    sql = multi_line_pattern.sub(replace_with_spaces, sql)
    
    return sql

# Example usage
sql_code = """
SELECT * FROM users -- now this is a comment
-- This is a single-line comment
WHERE id = 1;
/* This is a 
multi-line comment */
-- Another single-line comment
"""

clean_sql = replace_comments_with_spaces(sql_code)
print(clean_sql)
