"""Checker for drop cascade."""

from pglast import ast, enums, visitors

from pgshield.core import linter


class DropCascade(linter.BaseChecker):
    """## **What it does**
    Checks for usage of cascade update.

    ## **Why not?**
    Database schema should follow the principle of least surprise which
    says that every component in a system should behave in a way that most users
    expect it to behave, and therefore not surprise or astonish them.

    Cascading drops should not cause unexpected loss of data. It is certainly
    dangerous if dropping a single table can wipe out half your database.

    Are you certain you want cascade drop thus dropping every dependent objects?

    ## **When should you?**
    Almost never.

    ## **Use instead:**
    Restrict
    """
    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.behavior == enums.DropBehavior.DROP_CASCADE:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Drop cascade found",
                ),
            )

            if self.is_fix_applicable:

                node.behavior = enums.DropBehavior.DROP_RESTRICT
