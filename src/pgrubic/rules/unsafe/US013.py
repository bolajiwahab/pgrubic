"""Validating check constraint on existing rows."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class ValidatingCheckConstraintOnExistingRows(linter.BaseChecker):
    """## **What it does**
    Checks validating check constraint on existing rows.

    ## **Why not?**
    Adding a check constraint to an already populated table will have to scan and
    validate that there are no violating records in the table, causing the table to be
    locked in which no other operations can be performed on the table for the
    duration of the validation. This will cause downtime if the table is concurrently
    being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    1. Add the check constraint without validation.
    2. Validate the constraint in a separate transaction.
    """

    is_auto_fixable: bool = True

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and node.contype == enums.ConstrType.CONSTR_CHECK
            and not node.skip_validation
        ):
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Validating check constraint on existing rows",
                    auto_fixable=self.is_auto_fixable,
                    help="Add the check constraint without validation and validate it in a separate transaction",  # noqa: E501
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.Constraint) -> None:
        """Fix violation."""
        node.skip_validation = True
