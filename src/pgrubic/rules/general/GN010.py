"""Checker for table column conflict."""

from pglast import ast, enums, visitors

from pgrubic.core import linter
from pgrubic.rules.general import get_columns_from_table_creation


class TableColumnConflict(linter.BaseChecker):
    """## **What it does**
    Checks for duplicate columns.

    ## **Why not?**
    While each column in a table must have a unique name within that table to ensure
    unambiguous reference and avoid confusion during SQL operations, the name of a table
    should also be distinct from the name of its columns to avoid confusion and ensures
    clarity in database design and manipulation.

    ## **When should you?**
    Alsmost never.

    ## **Use instead:**
    Update conflicted name.
    """

    is_auto_fixable: bool = False

    def _register_violation(
        self,
        table_name: str,
        line_number: int,
        column_offset: int,
        source_text: str,
        statement_location: int,
    ) -> None:
        """Register the violation."""
        self.violations.add(
            linter.Violation(
                line_number=line_number,
                column_offset=column_offset,
                source_text=source_text,
                statement_location=statement_location,
                description=f"Table name '{table_name}' conflicts with the"
                " name of its columns",
            ),
        )

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        given_columns, _ = get_columns_from_table_creation(node)

        if node.relation.relname in given_columns:

            self._register_violation(
                table_name=node.relation.relname,
                line_number=self.line_number,
                column_offset=self.column_offset,
                source_text=self.source_text,
                statement_location=self.statement_location,
            )

    def visit_AlterTableStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableStmt,
    ) -> None:
        """Visit AlterTableStmt."""
        given_columns: list[str] = [
            cmd.def_.colname
            for cmd in node.cmds
            if cmd.subtype == enums.AlterTableType.AT_AddColumn
        ]

        if node.relation.relname in given_columns:

            self._register_violation(
                table_name=node.relation.relname,
                line_number=self.line_number,
                column_offset=self.column_offset,
                source_text=self.source_text,
                statement_location=self.statement_location,
            )
