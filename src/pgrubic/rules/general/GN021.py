"""Checker for unlogged table."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NullConstraint(linter.BaseChecker):
    """## **What it does**
    Checks for use of **NULL** constraint.

    ## **Why not?**
    From the documentation:

    The NOT NULL constraint has an inverse: the NULL constraint. This does not mean that
    the column must be null, which would surely be useless. Instead, this simply selects
    the default behavior that the column might be null. The NULL constraint is not present
    in the SQL standard and should not be used in portable applications.
    (It was only added to PostgreSQL to be compatible with some other database systems.)

    ## **When should you?**
    Almost Never.

    ## **Use instead:**
    Leave out NULL constraints.
    """

    is_auto_fixable: bool = True

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> visitors.ActionMeta | None:
        """Visit Constraint."""
        if node.contype == enums.ConstrType.CONSTR_NULL:

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="NULL constraints are redundant",
                ),
            )

            return self._fix()

        return None

    def _fix(self) -> visitors.ActionMeta:
        """Fix violation."""
        return visitors.Delete
