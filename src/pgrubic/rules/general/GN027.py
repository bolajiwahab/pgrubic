"""Checker for yoda conditions."""

import typing

from pglast import ast, enums, visitors

from pgrubic.core import linter


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

    operator_replacements: typing.ClassVar[dict[str, str]] = {
        ">": "<",
        "<": ">",
        ">=": "<=",
        "<=": ">=",
    }

    def visit_A_Expr(
        self,
        ancestors: visitors.Ancestor,
        node: ast.A_Expr,
    ) -> None:
        """Visit A_Expr."""
        if (
            node.kind == enums.A_Expr_Kind.AEXPR_OP
            and isinstance(
                node.lexpr,
                ast.A_Const,
            )
            and isinstance(node.rexpr, ast.ColumnRef)
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
                    description="Yoda conditions are discouraged",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Use natural condition",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.A_Expr) -> None:
        """Fix violation."""
        name = node.name
        # Adjust the operator accordingly
        name[-1].sval = self.operator_replacements.get(name[-1].sval, name[-1].sval)

        lexpr = node.lexpr
        rexpr = node.rexpr

        node.lexpr = rexpr
        node.rexpr = lexpr
        node.name = name
