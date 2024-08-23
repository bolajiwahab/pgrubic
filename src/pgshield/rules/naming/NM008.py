"""Checker for implicit constraint name."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class ImplicitConstraintName(linter.BaseChecker):
    """## **What it does**
    Checks that constraint is explicitly named and not relying on implicit naming.

    ## **Why not?**
    Explicitly naming a constraint is a good practice. It improves your code clarity and
    makes it more readable.

    A good naming convention makes your code easier to read and understand.

    ## **When should you?**
    Never almost.

    ## **Use instead:**
    Name your constraint according to the set naming convention.
    """
    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if not node.conname and node.contype in (
            enums.ConstrType.CONSTR_CHECK,
            enums.ConstrType.CONSTR_PRIMARY,
            enums.ConstrType.CONSTR_UNIQUE,
            enums.ConstrType.CONSTR_EXCLUSION,
            enums.ConstrType.CONSTR_FOREIGN,
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer named constraint",
                ),
            )
