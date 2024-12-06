"""Checker for non concurrent detach partition."""

from pglast import ast, visitors

from pgrubic.core import linter


class NonConcurrentDetachPartition(linter.BaseChecker):
    """## **What it does**
    Checks non-concurrent detach partition.

    ## **Why not?**
    Detaching a partition in non-concurrent mode acquires an **ACCESS EXCLUSIVE** lock on
    both the partition and the parent table, blocking other accesses to all partitions
    until the **DETACH PARTITION** is completed.
    This will cause downtime if the partitions are concurrently being accessed by other
    clients.

    Concurrent mode, **CONCURRENTLY** is a new feature from PostgreSQL 14.

    ## **When should you?**
    If the partitioned table is empty.
    If the partitioned table is not empty but is not being concurrently accessed.

    ## **Use instead:**
    From PostgreSQL 14, detach the partition in concurrent mode:
        **ALTER TABLE .. DETACH PARTITION .. CONCURRENTLY**
    """

    is_auto_fixable: bool = True

    def visit_PartitionCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.PartitionCmd,
    ) -> None:
        """Visit PartitionCmd."""
        detach_partition_concurrently_version = 14
        if (
            self.config.postgres_target_version >= detach_partition_concurrently_version
            and not node.concurrent
        ):
            self.violations.add(
                linter.Violation(
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Non concurrent detach partition",
                    auto_fixable=self.is_auto_fixable,
                    help="Detach the partition in concurrent mode",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.PartitionCmd) -> None:
        """Fix violation."""
        node.concurrent = True
