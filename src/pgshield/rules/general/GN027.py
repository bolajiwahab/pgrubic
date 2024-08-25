"""Checker for quoted NULL."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class YodaCondition(linter.BaseChecker):
    """## **What it does**
    Checks for yoda conditions.

    ## **Why not?**
    Yoda conditions can be harder to read and understand, especially for those who are not
    familiar with this syntax.

    Placing the constant on the left side makes it harder for someone to quickly grasp the
    meaning of the condition.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Natural condition.
    """

    is_auto_fixable: bool = True

    def visit_A_Expr(
        self,
        ancestors: visitors.Ancestor,
        node: ast.A_Expr,
    ) -> None:
        """Visit A_Expr."""
        if node.kind == enums.A_Expr_Kind.AEXPR_OP and isinstance(
            node.lexpr, ast.A_Const,
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Yoda conditions are discouraged",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.A_Expr) -> None:
        """Fix violation."""
        lexpr = node.lexpr
        rexpr = node.rexpr

        node.lexpr = rexpr
        node.rexpr = lexpr
