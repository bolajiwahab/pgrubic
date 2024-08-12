"""Unsafe index operations."""

from pglast import ast, enums

from pgshield.core import linter


class NonConcurrentReindex(linter.Checker):
    """Non concurrent reindex."""

    is_auto_fixable: bool = True

    def visit_ReindexStmt(self, ancestors: ast.Node, node: ast.ReindexStmt) -> None:
        """Visit ReindexStmt."""
        params = [param.defname for param in node.params] if node.params else []

        if (
            node.kind != enums.ReindexObjectType.REINDEX_OBJECT_SYSTEM
            and "concurrently" not in params
        ):

            self.violations.add(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent reindex",
                ),
            )

            if self.can_apply_fix:

                params.append(ast.DefElem(defname="concurrently"))

                node.params = params
