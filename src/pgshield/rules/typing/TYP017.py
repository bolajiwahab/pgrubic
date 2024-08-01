"""Checker for numeric with precision."""

from pglast import ast

from pgshield.core import linter


class NumericWithPrecision(linter.Checker):
    """## **What it does**
    Checks for usage of numeric with precision.

    ## **Why not?**
    Because it rounds off the fractional part which can lead to rounding errors slipping
    in when performing calculations and storing partial results before aggregation.

    ## **When should you?**
    When you want to, really. If what you want is a numeric field that will throw an
    error when you insert too large a value into it, and you don't want to use an
    explicit check constraint and you always want to store the fractional part in a
    specific decimal places then numeric(p, s) is a perfectly good type.
    Just don't use it automatically without thinking about it.

    ## **Use instead:**
    numeric.
    """
    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "numeric" and node.typeName.typmods:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer entire numeric",
                ),
            )

            if self.config.fix is True:

                node.typeName = ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": "numeric",
                        },
                    ),
                )
