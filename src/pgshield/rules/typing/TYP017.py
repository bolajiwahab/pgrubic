"""Checker for numeric with precision."""

from pglast import ast

from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


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

    name: str = "convention.prefer_entire_numeric"
    code: str = "TYP017"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if is_column_creation(ancestors) and (
            node.typeName.names[-1].sval == "timestamptz" and node.typeName.typmods
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer entire timestamp with timezone",
                ),
            )