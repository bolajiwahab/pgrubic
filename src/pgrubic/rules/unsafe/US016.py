"""Non-concurrent index creation."""

from pglast import ast, visitors

from pgrubic.core import linter


class NonConcurrentIndexCreation(linter.BaseChecker):
    """## **What it does**
    Checks non-concurrent index creation.

    ## **Why not?**
    Creating an index in non-concurrent mode will locks out writes (but not reads) on the
    table until it is done. This will cause downtime if the table is concurrently being
    written by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently written.

    ## **Use instead:**
    Create the index in concurrent mode: **CREATE .. INDEX CONCURRENTLY ON ..**.
    """

    is_auto_fixable: bool = True

    def visit_IndexStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
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
                    description="Non concurrent index creation",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Create the index in concurrent mode",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.IndexStmt) -> None:
        """Fix violation."""
        node.concurrent = True
