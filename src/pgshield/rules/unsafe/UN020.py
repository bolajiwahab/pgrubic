"""Unsafe index operations."""

import typing

from pglast import ast, enums, visitors

from pgshield.core import linter


class NonConcurrentReindex(linter.BaseChecker):
    """Non concurrent reindex."""

    is_auto_fixable: bool = True

    def visit_ReindexStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ReindexStmt,
    ) -> None:
        """Visit ReindexStmt."""
        params: list[typing.Any] = (
            [param.defname for param in node.params] if node.params else []
        )

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

            self._fix(node, params)

    def _fix(self, node: ast.ReindexStmt, params: list[typing.Any]) -> None:
        """Fix violation."""
        params.append(ast.DefElem(defname="concurrently"))

        node.params = params
