"""Checker for floating point types."""

from pglast import ast, visitors

from pgshield.core import linter


class Float(linter.BaseChecker):
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
    is_auto_fixable: bool = True

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if node.typeName.names[-1].sval in ["float4", "float8"]:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer numeric over float",
                ),
            )

            if self.is_fix_applicable:

                node.typeName = ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": "numeric",
                        },
                    ),
                )
