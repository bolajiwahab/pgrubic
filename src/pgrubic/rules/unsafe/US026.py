"""Checker for vacuum full."""

from pglast import ast, visitors

from pgrubic.core import linter


class VacuumFull(linter.BaseChecker):
    """## **What it does**
    Checks vacuum full.

    ## **Why not?**
    When a table is being vacuumed with the **FULL** option, an **ACCESS EXCLUSIVE** lock
    is acquired on it, preventing any other database operations (both reads and writes)
    from operating on the table until the **VACUUM FULL** is finished.
    This will cause downtime if the table is concurrently being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    Have a look at **pg_repack** as an alternative.
    """

    def visit_VacuumStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.VacuumStmt,
    ) -> None:
        """Visit VacuumStmt."""
        options = [option.defname for option in node.options] if node.options else []

        if "full" in options:
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Vacuum full found",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Have a look at pg_repack as an alternative",
                ),
            )
