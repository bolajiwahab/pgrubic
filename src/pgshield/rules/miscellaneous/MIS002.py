"""Checker for comparison with NULL."""

from pglast import ast

from pgshield.core import linter


class BooleanComparison(linter.Checker):
    """## **What it does**
    Checks for comparison with boolean values.

    ## **Why not?**
    The IS predicate always returns a boolean value, rather than propagating NULLs.

    ```sql
    SELECT null::boolean -- null
    SELECT null::boolean IS TRUE -- boolean false
    SELECT null::boolean IS NOT TRUE -- boolean true
    ```

    ## **When should you?**
    Propagation of NULLs wouldn't make a difference in a WHERE clause, because a NULL
    condition always excludes rows.

    ## **Use instead:**
    To check whether a value is a boolean, use the predicates:

        boolean_expression IS TRUE
        boolean_expression IS NOT TRUE
        boolean_expression IS FALSE
        boolean_expression IS NOT FALSE
        boolean_expression IS UNKNOWN
        boolean_expression IS NOT UNKNOWN
    """

    name: str = "miscellaneous.boolean_comparison"
    groups: tuple[str, ...] = ("convention", "miscellaneous")
    code: str = "MIS002"

    is_auto_fixable: bool = False

    def visit_A_Const(
        self,
        ancestors: ast.Node,
        node: ast.A_Const,
    ) -> None:
        """Visit A_Const."""
        if node.val and isinstance(node.val, ast.Boolean):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Use IS predicate for boolean values",
                ),
            )
