"""Checker for unlogged table."""

from pglast import ast, enums

from pgshield.core import linter


class CurrentTime(linter.Checker):
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
        ancestors: ast.Node,
        node: ast.SQLValueFunction,
    ) -> None:
        """Visit SQLValueFunction."""
        if node.op == enums.SQLValueFunctionOp.SVFOP_CURRENT_TIME:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer functions that return timestamps"
                                " instead of timetz",
                ),
            )

            if self.config.fix is True:

                node.op = enums.SQLValueFunctionOp.SVFOP_CURRENT_TIMESTAMP
