"""Checker for integer."""

from pglast import ast

from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


class Integer(linter.Checker):
    """## **What it does**
    Checks for usage of integer.

    ## **Why not?**
    Integer can store values up to 2.147 Billion which can lead to integer overflow once
    the max value is reached. The fire drill when you run out of integers is not cheap.

    ## **When should you?**
    Tables that store limited lookup options.

    ## **Use instead:**
    bigint.
    """

    name: str = "typing.prefer_bigint_over_int"
    code: str = "TYP010"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if is_column_creation(ancestors) and (node.typeName.names[-1].sval == "int4"):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer bigint over int",
                ),
            )
