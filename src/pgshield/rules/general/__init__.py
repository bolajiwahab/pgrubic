"""General rules."""

from pglast import ast


def get_column_details_from_table_creation(
    node: ast.CreateStmt,
) -> tuple[list[str], set[str]]:
    """Get column details from table creation."""
    if node.tableElts:

        given_columns: list[str] = [
            column.colname
            for column in node.tableElts
            if isinstance(column, ast.ColumnDef)
        ]

        duplicate_columns: set[str] = {
            column for column in given_columns if given_columns.count(column) > 1
        }

    return given_columns, duplicate_columns
