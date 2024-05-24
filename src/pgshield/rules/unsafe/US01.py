from pglast import ast
from linter import lint_rule

@lint_rule
def check_create_index_concurrently(visitor, node):
    if isinstance(node, ast.IndexStmt):
        if not node.concurrent:
            visitor.add_message(node, "Creating an index without 'CONCURRENTLY' can lock the table. Consider adding 'CONCURRENTLY'.")
