"""Checker for timestamp without time zone with precision."""

from pglast import ast, visitors

from pgshield.core import linter


class TimestampWithoutTimezoneWithPrecision(linter.BaseChecker):
    """## **What it does**
    Checks for usage of timestamp without time zone with precision.

    ## **Why not?**
    Because it rounds off the fractional part rather than truncating it as everyone
    would expect. This can cause unexpected issues; consider that when you store now()
    into such a column, you might be storing a value half a second in the future.

    ## **When should you?**
    Never.

    ## **Use instead:**
    timestamp (also known as timestamp without time zone) without precision.
    """
    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "timestamp" and node.typeName.typmods:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer entire timestamp without timezone",
                ),
            )

            if self.is_fix_applicable:

                node.typeName = ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": "timestamptz",
                        },
                    ),
                )
