"""Checker for quoted NULL."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class QuotedNull(linter.BaseChecker):
    """## **What it does**
    Checks for quoted NULL.

    ## **Why not?**
    Quoting NULL is an odd mistake to make.

    We should always use NULL without quotes when we intend to represent a null value.
    Quoting it, as in 'NULL', turns it into a string literal. Therefore, whether we are
    dealing with a null string or a null number, we must consistently use NULL without
    quotes across all data types.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Use NULL without quotes.
    """

    is_auto_fixable: bool = True

    def visit_A_Const(
        self,
        ancestors: visitors.Ancestor,
        node: ast.A_Const,
    ) -> ast.A_Const | None:
        """Visit A_Const."""
        if isinstance(node.val, ast.String) and node.val.sval.upper() == "NULL":

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Quoted NULL detected",
                ),
            )

            if self.is_fix_applicable:

                return ast.A_Const(isnull=True, val=ast.ValUnion(value=None))

        return node
