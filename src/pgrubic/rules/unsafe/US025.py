"""Checker for cluster."""

from pglast import ast, visitors

from pgrubic.core import linter


class Cluster(linter.BaseChecker):
    """## **What it does**
    Checks cluster.

    ## **Why not?**
    When a table is being clustered, an **ACCESS EXCLUSIVE** lock is acquired on it.
    This prevents any other database operations (both reads and writes) from operating on
    the table until the **CLUSTER** is finished.
    This will cause downtime if the table is concurrently being accessed by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    Have a look at pg_repack as an alternative.
    """

    def visit_ClusterStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ClusterStmt,
    ) -> None:
        """Visit ClusterStmt."""
        self.violations.add(
            linter.Violation(
                rule=self.code,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
                description="Cluster found",
                auto_fixable=self.is_auto_fixable,
                help="Have a look at pg_repack as an alternative",
            ),
        )
