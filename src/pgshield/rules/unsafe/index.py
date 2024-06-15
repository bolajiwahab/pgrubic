"""Unsafe index operations."""

from pglast import ast, enums, stream

from pgshield.core import linter


class NonConcurrentIndexCreation(linter.Checker):
    """Non concurrent index creation."""

    name = "unsafe.non_concurrent_index_creation"
    code = "UNI001"

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if not node.concurrent:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Non concurrent index creation",
                ),
            )


class IndexMovementToTablespace(linter.Checker):
    """Index movement to tablespace."""

    name = "unsafe.index_movement_to_tablespace"
    code = "UNI002"

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.AlterTableCmd) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors[statement_index].stmt.objtype == enums.ObjectType.OBJECT_INDEX
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Index movement to tablespace",
                ),
            )


class IndexesMovementToTablespace(linter.Checker):
    """Indexes movement to tablespace."""

    name = "unsafe.indexes_movement_to_tablespace"
    code = "UNI003"

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableMoveAllStmt,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.objtype == enums.ObjectType.OBJECT_INDEX:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Indexes movement to tablespace",
                ),
            )


class NonConcurrentIndexDrop(linter.Checker):
    """Non concurrent index drop."""

    name = "unsafe.non_concurrent_index_drop"
    code = "UNI004"

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.removeType == enums.ObjectType.OBJECT_INDEX and not node.concurrent:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Non concurrent index drop",
                ),
            )


class NonConcurrentReindex(linter.Checker):
    """Non concurrent reindex."""

    name = "unsafe.non_concurrent_reindex"
    code = "UNI005"

    def visit_ReindexStmt(self, ancestors: ast.Node, node: ast.ReindexStmt) -> None:
        """Visit ReindexStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        params = (
            [stream.RawStream()(param) for param in node.params]
            if node.params is not None
            else []
        )

        if params and "concurrently" not in params:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Non concurrent reindex",
                ),
            )
