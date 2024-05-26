import pglast
from pglast import parse_sql

# Example SQL query
sql_query = "SELECT * FROM my_table;"

# Parse the SQL query
parsed_tree = parse_sql(sql_query)

# Function to count the nodes in the AST
def count_nodes(node):
    count = 1  # Initialize with 1 for the current node
    if hasattr(node, 'nodes'):
        for child_node in node.nodes:
            count += count_nodes(child_node)
    return count

# Count the nodes in the AST
ast_length = count_nodes(parsed_tree)
print("Length of AST:", ast_length)
