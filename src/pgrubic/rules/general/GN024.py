"""Checker for comparison with NULL."""

from pglast import ast, enums, visitors

from pgrubic import Operators
from pgrubic.core import linter


class NullComparison(linter.BaseChecker):
    """## **What it does**
    Checks for comparison with NULL.

    ## **Why not?**
    Comparing NULL to NULL with = returns NULL, not true.
    Comparing a value to NULL returns neither true nor false, but NULL.

    Do not write expression = NULL because NULL is not equal to NULL.
    (The null value represents an unknown value, and it is not known whether two unknown
    values are equal.)

    ## **When should you?**
    Never.

    ## **Use instead:**
    To check whether a value is or is not null, use the predicates:

    - expression IS NULL
    - expression IS NOT NULL
    """

    is_auto_fixable: bool = True

    def visit_A_Expr(
        self,
        ancestors: visitors.Ancestor,
        node: ast.A_Expr,
    ) -> ast.NullTest:
        """Visit A_Expr."""
        if (
            node.kind == enums.A_Expr_Kind.AEXPR_OP
            and node.name[-1].sval in (Operators.EQ, Operators.NOT_EQ)
            and any(
                isinstance(expr, ast.A_Const) and expr.isnull
                for expr in (node.rexpr, node.lexpr)
            )
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
                    description="Comparison with NULL should be [IS | IS NOT] NULL",
                    auto_fixable=self.is_auto_fixable,
                    help="Use [IS | IS NOT] NULL",
                ),
            )

            return self._fix(node)

        return None  # pragma: no cover

    def _fix(self, node: ast.A_Expr) -> ast.NullTest:
        """Fix violation."""
        lexpr = (
            node.rexpr
            if not (isinstance(node.rexpr, ast.A_Const) and node.rexpr.isnull)
            else node.lexpr
        )

        null_type = (
            enums.NullTestType.IS_NULL
            if node.name[-1].sval == Operators.EQ
            else enums.NullTestType.IS_NOT_NULL
        )

        return ast.NullTest(arg=lexpr, nulltesttype=null_type)
