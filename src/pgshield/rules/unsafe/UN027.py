"""Unsafe table operations."""

from pglast import ast, visitors

from pgshield.core import linter


class NonConcurrentDetachPartition(linter.Checker):
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

            if self.is_fix_applicable:

                node.concurrent = True
