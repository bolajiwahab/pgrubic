"""Non concurrent index drop."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NonConcurrentIndexDrop(linter.BaseChecker):
    """## **What it does**
    Checks non-concurrent index drop.

    ## **Why not?**
    Dropping an index in non-concurrent mode acquires an **ACCESS EXCLUSIVE** lock on the
    table, blocking other accesses until the index drop is completed.
    This will cause downtime if the table is concurrently being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    Drop the index in concurrent mode: **DROP INDEX CONCURRENTLY ..**.
    """

    is_auto_fixable: bool = True

    def visit_DropStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_INDEX and not node.concurrent:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Non concurrent index drop",
                    auto_fixable=self.is_auto_fixable,
                    help="Drop the index in concurrent mode",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.DropStmt) -> None:
        """Fix violation."""
        node.concurrent = True
