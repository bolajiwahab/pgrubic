"""Checker for smallint."""

from pglast import ast

from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


class Smallint(linter.Checker):
    """## **What it does**
    Checks for usage of smallint.

    ## **Why not?**
    Smallint can store values up to 32767 which can lead to integer overflow once
    the max value is reached. The fire drill when you run out of integers is not cheap.

    ## **When should you?**
    Tables that store limited lookup options.

    ## **Use instead:**
    bigint.
    """

    name: str = "convention.prefer_bigint_over_smallint"
    code: str = "TYP011"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if is_column_creation(ancestors) and (node.typeName.names[-1].sval == "int2"):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer bigint over smallint",
                ),
            )
