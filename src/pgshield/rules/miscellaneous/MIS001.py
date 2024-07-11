"""Checker for comparison with NULL."""

from pglast import ast

from pgshield.core import linter


class NullComparison(linter.Checker):
    """## **What it does**
    Checks for comparison with NULL.

    ## **Why not?**
    Comparing NULL to NULL with = returns NULL, not true.
    Comparing a value to NULL returns neither true nor false, but NULL.

    Do not write expression = NULL because NULL is not “equal to” NULL.
    (The null value represents an unknown value, and it is not known whether two unknown
    values are equal.)

    ## **When should you?**
    Never.

    ## **Use instead:**
    To check whether a value is or is not null, use the predicates:

        expression IS NULL
        expression IS NOT NULL
    """

    name: str = "miscellaneous.null_comparison"
    groups: tuple[str, ...] = ("convention", "miscellaneous")
    code: str = "MIS001"

    is_auto_fixable: bool = False

    def visit_A_Const(
        self,
        ancestors: ast.Node,
        node: ast.A_Const,
    ) -> None:
        """Visit A_Const."""
        if node.isnull:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Do not compare with NULL",
                ),
            )
