"""Checker for stringified NULL."""

from pglast import ast, enums, visitors

from pgrubic import Operators
from pgrubic.core import linter


class StringifiedNull(linter.BaseChecker):
    """## **What it does**
    Checks for stringified NULL.

    ## **Why not?**
    NULL is not a data value, but a marker for an absent value, and it should not be
    quoted.

    Putting NULL in quotes makes it a string value, which is not the same as a NULL value.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Use NULL without quotes.
    """

    is_auto_fixable: bool = True

    def visit_String(
        self,
        ancestors: visitors.Ancestor,
        node: ast.String,
    ) -> ast.A_Const:
        """Visit String that is not part of an A_Expr."""
        if node.sval.upper() == "NULL" and not ancestors.find_nearest(ast.A_Expr):
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Quoted NULL detected",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Remove quotes from NULL",
                ),
            )

            return self._fix_string(node=node)

        return None

    def _fix_string(self, node: ast.String) -> ast.A_Const:
        """Fix string violation."""
        return ast.A_Const(
            isnull=True,
            val=ast.ValUnion(value=node),
        )

    def visit_A_Expr(
        self,
        ancestors: visitors.Ancestor,
        node: ast.A_Expr,
    ) -> ast.NullTest:
        """Visit A_Expr."""
        if (
            isinstance(node.lexpr, ast.A_Const)
            and isinstance(node.lexpr.val, ast.String)
            and node.lexpr.val.sval.upper() == "NULL"
        ) or (
            isinstance(node.rexpr, ast.A_Const)
            and isinstance(node.rexpr.val, ast.String)
            and node.rexpr.val.sval.upper() == "NULL"
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
                    description="Quoted NULL detected",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Remove quotes from NULL",
                ),
            )

            return self._fix_expression(node=node)

        return None  # pragma: no cover

    def _fix_expression(self, node: ast.A_Expr) -> ast.A_Const:
        """Fix expression violation."""
        if not isinstance(node.rexpr, ast.A_Const) or (
            isinstance(node.rexpr, ast.A_Const)
            and isinstance(node.rexpr.val, ast.String)
            and node.rexpr.val.sval.upper() != "NULL"
        ):
            lexpr = node.rexpr
        else:
            lexpr = node.lexpr

        null_type = (
            enums.NullTestType.IS_NULL
            if node.name[-1].sval == Operators.EQ
            else enums.NullTestType.IS_NOT_NULL
        )

        return ast.NullTest(arg=lexpr, nulltesttype=null_type)
