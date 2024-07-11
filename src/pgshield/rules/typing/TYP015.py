"""Checker for blacklisted data types."""

from pglast import ast

from pgshield.core import linter
from pgshield.rules.typing import is_column_creation


class BlacklistedDataTypes(linter.Checker):
    """## **What it does**
    Checks for usage of blacklisted data types.

    ## **Why not?**
    If you are using a blacklisted type, you're probably doing something wrong.

    ## **When should you?**
    Never. If a data type is intended to be used, it should not be in the blacklist.

    ## **Use instead:**
    Data types that are not in the blacklist.
    """

    name: str = "convention.blacklisted_type"
    code: str = "TYP015"

    is_auto_fixable: bool = False

    def visit_TypeName(
        self,
        ancestors: ast.Node,
        node: ast.TypeName,
    ) -> None:
        """Visit TypeName."""
        if (
            is_column_creation(ancestors)
            and node.names[-1].sval in self.config.blacklisted_types
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Data type '{node.names[-1].sval}' is blacklisted",
                ),
            )
