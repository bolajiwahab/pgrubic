"""Non concurrent reindex."""

import typing

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NonConcurrentReindex(linter.BaseChecker):
    """## **What it does**
    Checks non-concurrent reindex.

    ## **Why not?**
    Reindexing in non-concurrent mode will locks out writes (but not reads) on
    the table until it is done. This will cause downtime if the table is concurrently
    being written by other clients.

    ## **When should you?**
    If the table is empty.
    If the table is not empty but is not being concurrently written.

    ## **Use instead:**
    Reindex in concurrent mode: **REINDEX .. CONCURRENTLY ..**.
    """

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
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Non concurrent reindex",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Reindex in concurrent mode",
                ),
            )

            self._fix(node, params)

    def _fix(self, node: ast.ReindexStmt, params: list[typing.Any]) -> None:
        """Fix violation."""
        params.append(ast.DefElem(defname="concurrently"))

        node.params = params
