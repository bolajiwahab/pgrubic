"""Checker for quoted NULL."""

from pglast import ast, visitors

from pgrubic.core import linter


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

    def visit_String(
        self,
        ancestors: visitors.Ancestor,
        node: ast.String,
    ) -> ast.String | None:
        """Visit String."""
        if node.sval.upper() == "NULL":

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Quoted NULL detected",
                ),
            )

            return self._fix()

        return node

    def _fix(self) -> ast.String | None:
        """Fix violation."""
        return ast.A_Const(isnull=True, val=ast.ValUnion(value=None))
