"""Checker for smallint."""

from pglast import ast

from pgshield.core import linter


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
    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval == "int2":

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer bigint over smallint",
                ),
            )

            if self.config.fix is True:

                node.typeName = ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": "bigint",
                        },
                    ),
                )
