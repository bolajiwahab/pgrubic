"""Checker for rule."""
from pglast import ast

from pgshield.core import linter


class CreateRule(linter.Checker):
    """## **What it does**
    Checks for creation of rules.

    ## **Why not?**
    Rules are incredibly powerful, but they don't do what they look like they do.
    They look like they're some conditional logic, but they actually rewrite a query
    to modify it or add additional queries to it.

    ## **When should you?**
    Never. While the rewriter is an implementation detail of VIEWs,
    there is no reason to pry up this cover plate directly.

    ## **Use instead:**
    Don't use rules. If you think you want to, use a trigger instead.
    """

    name: str = "general.create_rule"
    code: str = "GN002"

    is_auto_fixable: bool = False

    def visit_RuleStmt(
        self,
        ancestors: ast.Node,
        node: ast.RuleStmt,
    ) -> None:
        """Visit RuleStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Prefer trigger over rule",
            ),
        )
