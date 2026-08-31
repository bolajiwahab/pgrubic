"""Checker for table column conflict."""

import typing

from pglast import ast, enums, visitors

from pgrubic.core import linter
from pgrubic.rules.general import get_columns_from_table_creation


class TableColumnConflict(linter.BaseChecker):
    """## **What it does**
    Checks for table column conflict.

    ## **Why not?**
    While each column in a table must have a unique name within that table to ensure
    unambiguous reference and avoid confusion during SQL operations, the name of a table
    should also be distinct from the name of its columns to avoid confusion and ensures
    clarity in database design and manipulation.

    ## **When should you?**
    Almost never.

    ## **Use instead:**
    Resolve the name conflict.
    """

    def _register_violation(
        self,
        table_name: str,
        line_number: int,
        column_offset: int,
        line: str,
        statement_location: int,
    ) -> None:
        """Register the violation."""
        self.violations.add(
            linter.Violation(
                rule_code=self.code,
                rule_name=self.name,
                rule_category=self.category,
                line_number=line_number,
                column_offset=column_offset,
                line=line,
                statement_location=statement_location,
                description=f"Table name `{table_name}` conflicts with the"
                " name of its column(s)",
                is_auto_fixable=self.is_auto_fixable,
                is_fix_enabled=self.is_fix_enabled,
                help="Resolve the name conflict",
            ),
        )

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        relation = typing.cast(ast.RangeVar, node.relation)
        relation_name = typing.cast(str, relation.relname)
        given_columns, _ = get_columns_from_table_creation(node)

        if any(column.name == relation_name for column in given_columns):
            self._register_violation(
                table_name=relation_name,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
            )

    def visit_AlterTableStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableStmt,
    ) -> None:
        """Visit AlterTableStmt."""
        relation = typing.cast(ast.RangeVar, node.relation)
        relation_name = typing.cast(str, relation.relname)
        commands = typing.cast(tuple[ast.AlterTableCmd, ...], node.cmds)
        given_columns: list[str] = []
        for cmd in commands:
            if cmd.subtype == enums.AlterTableType.AT_AddColumn:
                column_definition = typing.cast(ast.ColumnDef, cmd.def_)
                given_columns.append(typing.cast(str, column_definition.colname))

        if relation_name in given_columns:
            self._register_violation(
                table_name=relation_name,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
            )
