"""Checker for missing replace in view."""

from pglast import ast, visitors

from pgrubic.core import linter


class MissingReplaceInFunction(linter.BaseChecker):
    """## **What it does**
    Checks for replace in view creation.

    ## **Why not?**
    `CREATE OR REPLACE VIEW` simplifies the process of modifying existing functions,
    as you don't need to manually drop and recreate them.

    If you drop and then recreate a view, the new view is not the same entity as
    the old; you will have to drop existing rules, views, triggers, etc. that refer to the
    old view. Use CREATE OR REPLACE VIEW to change a view definition without
    breaking objects that refer to the view. It also maintains data integrity and
    consistency.

    ## **When should you?**
    If you don't need to modify an existing view.

    ## **Use instead:**
    CREATE OR REPLACE VIEW.
    """

    is_auto_fixable: bool = True

    def visit_ViewStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ViewStmt,
    ) -> None:
        """Visit ViewStmt."""
        if not node.replace:
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Prefer create or replace for view",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.ViewStmt) -> None:
        """Fix violation."""
        node.replace = True
