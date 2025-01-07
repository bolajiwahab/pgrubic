"""Checker for non concurrent refresh materialized view."""

from pglast import ast, visitors

from pgrubic.core import linter


class NonConcurrentRefreshMaterializedView(linter.BaseChecker):
    """## **What it does**
    Checks non-concurrent refresh materialized view.

    ## **Why not?**
    Refreshing a materialized view in non-concurrent mode will locks out reads on the
    materialized view until it is done. This will cause downtime if the materialized view
    is concurrently being read by other clients.

    ## **When should you?**
    If downtime is acceptable.

    ## **Use instead:**
    Refresh the materialized view in concurrent mode:
        **REFRESH MATERIALIZED VIEW CONCURRENTLY ..**

    Please note that **CONCURRENTLY** option is only allowed if there is at least one
    UNIQUE index on the materialized view which uses only column names and includes all
    rows; that is, it must not be an expression index or include a WHERE clause.
    """

    is_auto_fixable: bool = True

    def visit_RefreshMatViewStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.RefreshMatViewStmt,
    ) -> None:
        """Visit RefreshMatViewStmt."""
        if not node.concurrent:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Non concurrent refresh materialized view",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Refresh the materialized view in concurrent mode",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.PartitionCmd) -> None:
        """Fix violation."""
        node.concurrent = True
