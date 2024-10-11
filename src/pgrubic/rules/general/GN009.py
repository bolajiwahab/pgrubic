"""Checker for duplicate columns."""

from pglast import ast, visitors

from pgrubic.core import linter
from pgrubic.rules.general import get_columns_from_table_creation


class DuplicateColumn(linter.BaseChecker):
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

    is_auto_fixable: bool = False

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        _, duplicate_columns = get_columns_from_table_creation(node)

        for column in duplicate_columns:
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Column `{column}` specified more than once",
                ),
            )
