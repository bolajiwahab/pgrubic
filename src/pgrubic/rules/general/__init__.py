"""General rules."""

import typing

from pglast import ast

from pgrubic.core import config


def get_columns_from_table_creation(
    node: ast.CreateStmt,
) -> tuple[list[config.Column], set[str]]:
    """Get column details from table creation."""
    given_columns: list[config.Column] = []
    duplicate_columns: set[str] = set()

    if node.tableElts:
        column_definitions = [
            column for column in node.tableElts if isinstance(column, ast.ColumnDef)
        ]

        for column in column_definitions:
            column_name = typing.cast(str, column.colname)
            type_name = typing.cast(ast.TypeName, column.typeName)
            type_names = typing.cast(
                tuple[ast.String, ...],
                type_name.names,
            )
            data_type = typing.cast(str, type_names[-1].sval)
            given_columns.append(
                config.Column(
                    name=column_name,
                    data_type=data_type,
                ),
            )

        columns: list[str] = [column.name for column in given_columns]

        duplicate_columns = {column for column in columns if columns.count(column) > 1}

    return given_columns, duplicate_columns
