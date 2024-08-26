"""Unsafe table operations."""

from pglast import ast, visitors

from pgshield.core import linter


class NonConcurrentDetachPartition(linter.BaseChecker):
    """Detach partition."""
    is_auto_fixable: bool = False

    def visit_PartitionCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.PartitionCmd,
    ) -> None:
        """Visit PartitionCmd."""
        if not node.concurrent:

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent detach partition",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.PartitionCmd) -> None:
        """Fix violation."""
        node.concurrent = True
