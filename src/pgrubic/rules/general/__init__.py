"""General rules."""

from pglast import ast

from pgrubic.core import config


def get_columns_from_table_creation(
    node: ast.CreateStmt,
) -> tuple[list[config.Column], set[str]]:
    """Get column details from table creation."""
    given_columns: list[config.Column] = []
    duplicate_columns: set[str] = set()

    if node.tableElts:

        given_columns = [
            config.Column(
                name=column.colname,
                data_type=column.typeName.names[-1],
            )
            for column in node.tableElts
            if isinstance(column, ast.ColumnDef)
        ]

        columns: list[str] = [column.name for column in given_columns]

        duplicate_columns = {column for column in columns if columns.count(column) > 1}

    return given_columns, duplicate_columns
