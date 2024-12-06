"""Checker for not null constraint on existing column."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NotNullConstraintOnExistingColumn(linter.BaseChecker):
    """## **What it does**
    Checks **NOT NULL** constraint on an existing column.

    ## **Why not?**
    Adding a **NOT NULL** constraint to an existing column of an already populated table
    will have to scan and validate that there are no nulls in the column, causing the
    table to be locked in which no other operations can be performed on the table for the
    duration of the validation. This will cause downtime if the table is concurrently
    being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    1. Create a check constraint: **CHECK (column IS NOT NULL) NOT VALID**.
    2. Validate the constraint.
    3. Set the column as NOT NULL.
    4. Drop the constraint.
    """

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_SetNotNull:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Not null constraint on existing column `{node.name}`",
                    auto_fixable=self.is_auto_fixable,
                    help="Add a supporting check constraint",
                ),
            )
