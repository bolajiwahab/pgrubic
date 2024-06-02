"""Unsafe index operations."""

from pglast import ast, enums, stream  # type: ignore[import-untyped]

from pgshield import utils, linter


class NonConcurrentIndexCreation(linter.Checker):  # type: ignore[misc]
    """Non concurrent index creation."""

    name = "unsafe.non_concurrent_index_creation"
    code = "UNI001"

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit IndexStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            not node.concurrent
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent index creation",
                ),
            )


class IndexMovementToTablespace(linter.Checker):
    """Index movement to tablespace."""

    name = "unsafe.index_movement_to_tablespace"
    code = "UNI002"

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors[statement_index].stmt.objtype == enums.ObjectType.OBJECT_INDEX
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
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
        node: ast.Node,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.objtype == enums.ObjectType.OBJECT_INDEX
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
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
        node: ast.Node,
    ) -> None:
        """Visit DropStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.removeType == enums.ObjectType.OBJECT_INDEX
            and not node.concurrent
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent index drop",
                ),
            )


class NonConcurrentReindex(linter.Checker):
    """Non concurrent reindex."""

    name = "unsafe.non_concurrent_reindex"
    code = "UNI005"

    def visit_ReindexStmt(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit ReindexStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        params = (
            [stream.RawStream()(param) for param in node.params]
            if node.params is not None
            else []
        )

        if (
            "concurrently" not in params
            and (
                ancestors[statement_index].stmt_location,
                self.code,
            )
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent reindex",
                ),
            )

