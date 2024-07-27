"""Unsafe table operations."""

from pglast import ast

from pgshield.core import linter


class NonConcurrentDetachPartition(linter.Checker):
    """Detach partition."""

    name: str = "unsafe.detach_partition"
    code: str = "UST007"

    is_auto_fixable: bool = False

    def visit_PartitionCmd(
        self,
        ancestors: ast.Node,
        node: ast.PartitionCmd,
    ) -> None:
        """Visit PartitionCmd."""
        if not node.concurrent:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent detach partition",
                ),
            )

