"""Checker for floating point types."""
from pglast import ast

from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


class Float(linter.Checker):
    """## **What it does**
    Checks for usage of float types.

    ## **Why not?**
    Floating point types are inexact, variable-precision numeric types.
    Inexact means that some values cannot be converted exactly to the internal format
    and are stored as approximations, so that storing and retrieving a value might show
    slight discrepancies.

    Comparing two floating-point values for equality might not always work as expected.

    ## **When should you?**
    When approximates are acceptable, no comparison for equality is needed.

    ## **Use instead:**
    1. numeric
    2. decimal
    """

    name: str = "convention.prefer_numeric_over_float"
    code: str = "TYP012"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if is_column_creation(ancestors) and (
            node.typeName.names[-1].sval in ["float4", "float8"]
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer numeric over float",
                ),
            )
