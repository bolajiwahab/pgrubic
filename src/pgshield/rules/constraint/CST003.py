"""Checker for identity generated by default."""
from pglast import ast, enums

from pgshield.core import linter


class IdentityGeneratedByDefault(linter.Checker):
    """## **What it does**
    Checks for identity generated by default.

    ## **Why not?**
    **GENERATED BY DEFAULT** allows you to specify a value for insert or update on an
    identity column instead of system generated value. This is usually not what you
    want for an identity column.

    ## **When should you?**
    If you want to be able to specify a value for insert or update on an identity
    column instead of system generated value.

    ## **Use instead:**
    **GENERATED ALWAYS**
    """

    name: str = "constraint.identity_generated_by_default"
    code: str = "CST004"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_IDENTITY
            and node.generated_when == enums.ATTRIBUTE_IDENTITY_BY_DEFAULT
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer generated always over generated by default identity",  # noqa: E501
                ),
            )
