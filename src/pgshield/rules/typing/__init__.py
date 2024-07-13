"""Rules for typing."""

from pglast import ast


def is_column_creation(ancestors: ast.Node) -> bool:
    """Check ancestors for column creation."""
    return ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors

