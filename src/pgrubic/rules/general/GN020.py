"""Checker for unlogged table."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class CurrentTime(linter.BaseChecker):
    """## **What it does**
    Checks for use of **CURRENT_TIME** function.

    ## **Why not?**
    It returns a value of type timetz, for which see [TYP002](www.placeholder.com).

    ## **When should you?**
    Never.

    ## **Use instead:**
    Do not use the CURRENT_TIME function. Use whichever of these is appropriate:
    - CURRENT_TIMESTAMP or now() if you want a timestamp with time zone,
    - LOCALTIMESTAMP if you want a timestamp without time zone,
    - CURRENT_DATE if you want a date,
    - LOCALTIME if you want a time
    """

    is_auto_fixable: bool = True

    def visit_SQLValueFunction(
        self,
        ancestors: visitors.Ancestor,
        node: ast.SQLValueFunction,
    ) -> None:
        """Visit SQLValueFunction."""
        if node.op == enums.SQLValueFunctionOp.SVFOP_CURRENT_TIME:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Prefer functions that return timestamptz"
                    " instead of timetz",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.SQLValueFunction) -> None:
        """Fix violation."""
        node.op = enums.SQLValueFunctionOp.SVFOP_CURRENT_TIMESTAMP
