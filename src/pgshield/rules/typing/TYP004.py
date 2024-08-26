"""Checker for timestamp with time zone with precision."""

from pglast import ast, visitors

from pgshield.core import linter


class TimestampWithTimezoneWithPrecision(linter.BaseChecker):
    """## **What it does**
    Checks for usage of timestamp with time zone with precision.

    ## **Why not?**
    Because it rounds off the fractional part rather than truncating it as everyone
    would expect. This can cause unexpected issues; consider that when you store now()
    into such a column, you might be storing a value half a second in the future.

    ## **When should you?**
    Never.

    ## **Use instead:**
    timestamptz (also known as timestamp with time zone) without precision.
    """
    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "timestamptz" and node.typeName.typmods:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer entire timestamp with timezone",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.ColumnDef) -> None:
        """Fix violation."""
        node.typeName = ast.TypeName(
            names=(
                {
                    "@": "String",
                    "sval": "timestamptz",
                },
            ),
        )
