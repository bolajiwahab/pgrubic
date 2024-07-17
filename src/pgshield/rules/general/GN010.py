"""Checker for table column conflict."""

from pglast import ast, enums

from pgshield.core import linter
from pgshield.rules.general import get_column_details_from_table_creation


class TableColumnConflict(linter.Checker):
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

    name: str = "general.table_column_conflict"
    code: str = "GN010"

    is_auto_fixable: bool = True

    def _register_violation(
        self,
        table_name: str,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Register the violation."""
        self.violations.append(
            linter.Violation(
                statement_location=statement_location,
                statement_length=statement_length,
                node_location=node_location,
                description=f"Table name '{table_name}' conflicts with the"
                " name of its columns",
            ),
        )

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        given_columns, _ = get_column_details_from_table_creation(node)

        if node.relation.relname in given_columns:

            self._register_violation(
                table_name=node.relation.relname,
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
            )

    def visit_AlterTableStmt(
        self,
        ancestors: ast.Node,
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
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
            )
