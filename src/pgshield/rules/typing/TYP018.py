"""Checker for nullable boolean field."""
from pglast import ast, enums

from pgshield.core import linter


class NullableBooleanField(linter.Checker):
    """## **What it does**
    Checks for usage of numeric with precision.

    ## **Why not?**
    3 possible values is not a boolean. By allowing nulls in a boolean field, you are
    turning an intended binary representation (true/false) into a ternary representation
    (true, false, null). Null is neither 'true' nor 'false'.
    Allowing nulls in a boolean field is an oversight that leads to unnecessarily
    ambiguous data.

    ## **When should you?**
    Never.

    ## **Use instead:**
    boolean with not null constraint.
    """

    name: str = "typing.nullable_boolean_field"
    code: str = "TYP018"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors
        ) and node.typeName.names[-1].sval == "bool":

            is_not_null = bool(
                (
                    [
                        constraint
                        for constraint in node.constraints
                        if constraint.contype == enums.ConstrType.CONSTR_NOTNULL
                    ]
                    if node.constraints is not None
                    else []
                ),
            )

            if not is_not_null:

                self.violations.append(
                    linter.Violation(
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                        description="Boolean field should be non-nullable",
                    ),
                )
