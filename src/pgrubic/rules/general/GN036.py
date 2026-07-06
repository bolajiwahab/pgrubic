"""Checker for self assigning column."""

from pglast import ast, visitors

from pgrubic import get_fully_qualified_name
from pgrubic.core import linter


class SelfAssigningColumn(linter.BaseChecker):
    """## **What it does**
    Checks for self assigning columns.

    ## **Why not?**
    Assigning a column to itself does not change its value but still causes PostgreSQL to
    process the row as an update, create a new row version, creating unnecessary write
    amplification, dead tuples, WAL, and potential table and index bloats.

    In most cases, this assignment is redundant or indicates that a different value was
    intended.

    ## **When should you?**
    Almost never. Intentional self-assignments are rare and are typically used only to
    force UPDATE semantics, such as firing triggers.

    ## **Use instead:**
    Use the correct value or remove the assignment entirely.
    """

    def visit_ResTarget(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ResTarget,
    ) -> None:
        """Visit ResTarget."""
        if (
            ancestors.find_nearest(ast.UpdateStmt)
            and isinstance(node.val, ast.ColumnRef)
            and node.name == get_fully_qualified_name(node.val.fields)
        ):
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Self assigning column",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Avoid self-assignments in UPDATE statements",
                ),
            )
