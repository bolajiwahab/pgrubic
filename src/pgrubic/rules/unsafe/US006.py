"""Checker for adding of stored generated column."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class AddingStoredGeneratedColumn(linter.BaseChecker):
    """## **What it does**
    Checks adding of stored generated column.

    ## **Why not?**
    Adding an stored generated column to an already populated table will
    have to backfill the newly added column, causing the table to be locked
    in which no other operations can be performed on the table for the duration
    of the backfill. This will cause downtime if the table is concurrently
    being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    A trigger might be a safer option.
    """

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and node.contype == enums.ConstrType.CONSTR_GENERATED
        ):
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Adding stored generated column is not safe",
                    auto_fixable=self.is_auto_fixable,
                    help="A trigger might be a safer option",
                ),
            )
