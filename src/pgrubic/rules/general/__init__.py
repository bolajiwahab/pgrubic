"""General rules."""

from pglast import ast


def get_columns_from_table_creation(
    node: ast.CreateStmt,
) -> tuple[list[str], set[str]]:
    """Get column details from table creation."""
    given_columns: list[str] = []
    duplicate_columns: set[str] = set()

    if node.tableElts:

        given_columns = [
            column.colname
            for column in node.tableElts
            if isinstance(column, ast.ColumnDef)
        ]

        duplicate_columns = {
            column for column in given_columns if given_columns.count(column) > 1
        }

    return given_columns, duplicate_columns
