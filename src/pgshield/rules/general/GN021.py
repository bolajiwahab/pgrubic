"""Checker for unlogged table."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class NullConstraint(linter.Checker):
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
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> visitors.ActionMeta | None:
        """Visit Constraint."""
        if node.contype == enums.ConstrType.CONSTR_NULL:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="NULL constraints are redundant",
                ),
            )

            if self.config.fix is True:

                return visitors.Delete

        return None

