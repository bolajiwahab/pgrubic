"""Checker for duplicate columns."""

from pglast import ast

from pgshield.core import linter
from pgshield.rules.general import get_columns_from_table_creation


class DuplicateColumn(linter.Checker):
    """## **What it does**
    Checks for duplicate columns.

    ## **Why not?**
    Each column in a table must have a unique name within that table to ensure unambiguous
    reference and avoid confusion during SQL operations. It ensures data integrity and
    clarity in database design and manipulation.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Remove duplicate columns.
    """

    name: str = "general.duplicate_column"
    code: str = "GN009"

    is_auto_fixable: bool = False

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        _, duplicate_columns = get_columns_from_table_creation(node)

        for column in duplicate_columns:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Column '{column}' specified more than once",
                ),
            )
