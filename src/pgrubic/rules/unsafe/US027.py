"""Checker for non concurrent detach partition."""

from pglast import ast, visitors

from pgrubic.core import linter


class NonConcurrentDetachPartition(linter.BaseChecker):
    """Detach partition."""

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
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.PartitionCmd) -> None:
        """Fix violation."""
        node.concurrent = True
