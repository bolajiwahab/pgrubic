"""Unsafe index operations."""

from pglast import ast, enums, stream

from pgshield.core import linter


class NonConcurrentIndexCreation(linter.Checker):
    """Non concurrent index creation."""

    name = "unsafe.non_concurrent_index_creation"
    code = "UNI001"

    is_auto_fixable: bool = False

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        if not node.concurrent:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent index creation",
                ),
            )


class IndexMovementToTablespace(linter.Checker):
    """Index movement to tablespace."""

    name = "unsafe.index_movement_to_tablespace"
    code = "UNI002"

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.AlterTableCmd) -> None:
        """Visit AlterTableCmd."""
        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors[2].stmt.objtype == enums.ObjectType.OBJECT_INDEX
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Index movement to tablespace",
                ),
            )


class IndexesMovementToTablespace(linter.Checker):
    """Indexes movement to tablespace."""

    name = "unsafe.indexes_movement_to_tablespace"
    code = "UNI003"

    is_auto_fixable: bool = False

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableMoveAllStmt,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        if node.objtype == enums.ObjectType.OBJECT_INDEX:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Indexes movement to tablespace",
                ),
            )


class NonConcurrentIndexDrop(linter.Checker):
    """Non concurrent index drop."""

    name = "unsafe.non_concurrent_index_drop"
    code = "UNI004"

    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_INDEX and not node.concurrent:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent index drop",
                ),
            )


class NonConcurrentReindex(linter.Checker):
    """Non concurrent reindex."""

    name = "unsafe.non_concurrent_reindex"
    code = "UNI005"

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
