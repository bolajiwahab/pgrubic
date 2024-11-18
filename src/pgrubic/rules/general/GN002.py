"""Checker for rule."""

from pglast import ast, visitors

from pgrubic.core import linter


class CreateRule(linter.BaseChecker):
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

    def visit_RuleStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RuleStmt,
    ) -> None:
        """Visit RuleStmt."""
        self.violations.add(
            linter.Violation(
                rule=self.code,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
                description="Create rule detected",
            ),
        )
