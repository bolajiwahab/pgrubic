"""Checker for time with time zone."""

from pglast import ast

from pgshield.core import linter


class TimeWithTimeZone(linter.Checker):
    """## **What it does**
    Checks for usage of time with time zone.

    ## **Why not?**
    Even the manual tells you it is only implemented for SQL compliance:

    > The type time with time zone is defined by the SQL standard, but the definition
    > exhibits properties which lead to questionable usefulness. In most cases,
    > a combination of date, time, timestamp without time zone, and
    > timestamp with time zone should provide a complete range of date/time
    > functionality required by any application.

    ## **When should you?**
    Never.

    ## **Use instead:**
    timestamptz (also known as timestamp with time zone).
    """
    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "timetz":

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer timestamp with timezone over time with timezone",
                ),
            )

            if self.config.fix is True:

                node.typeName = ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": "timestamptz",
                        },
                    ),
                )
