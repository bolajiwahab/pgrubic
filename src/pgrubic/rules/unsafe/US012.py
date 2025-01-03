"""Validating foreign key constraint on existing rows."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class ValidatingForeignKeyConstraintOnExistingRows(linter.BaseChecker):
    """## **What it does**
    Checks validating foreign key constraint on existing rows.

    ## **Why not?**
    Adding a foreign key constraint to an already populated table will have to scan and
    validate that there are no violating records in the table, causing the table to be
    locked in which no other operations can be performed on the table for the
    duration of the validation. This will cause downtime if the table is concurrently
    being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    1. Add the foreign key constraint without validation.
    2. Validate the constraint in a separate transaction.
    """

    is_auto_fixable = True

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and node.contype == enums.ConstrType.CONSTR_FOREIGN
            and not node.skip_validation
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
                    description="Validating foreign key constraint on existing rows",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Add the foreign key constraint without validation and validate it in a separate transaction",  # noqa: E501
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.Constraint) -> None:
        """Fix violation."""
        node.skip_validation = True
