"""Checker for creation of enum."""

from pglast import ast, visitors

from pgshield.core import linter


class CreateEnum(linter.Checker):
    """## **What it does**
    Checks for creation of enum.

    ## **Why not?**
    Enum types are primarily intended for static sets of values, though there is support
    for adding new values to an existing enum type, and for renaming values however
    existing values cannot be removed from an enum type, nor can the sort ordering of
    such values be changed, short of dropping and re-creating the enum type.

    ## **When should you?**
    If your set of values are fixed such that you won't be removing values
    in the future. Just don't use it automatically without thinking about it.

    ## **Use instead:**
    Mapping table.
    """
    is_auto_fixable: bool = False

    def visit_CreateEnumStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        self.violations.add(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Prefer mapping table to enum",
            ),
        )
