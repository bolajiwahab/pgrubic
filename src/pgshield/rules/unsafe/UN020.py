"""Unsafe index operations."""

from pglast import ast, stream

from pgshield.core import linter


class NonConcurrentReindex(linter.Checker):
    """Non concurrent reindex."""
    is_auto_fixable: bool = False

    def visit_ReindexStmt(self, ancestors: ast.Node, node: ast.ReindexStmt) -> None:
        """Visit ReindexStmt."""
        params = (
            [stream.RawStream()(param) for param in node.params]
            if node.params is not None
            else []
        )

        if params and "concurrently" not in params:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent reindex",
                ),
            )
