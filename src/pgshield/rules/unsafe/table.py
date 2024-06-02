"""Unsafe table operations."""

from pglast import ast, enums, stream  # type: ignore[import-untyped]

from pgshield import utils, linter


class DropTable(linter.Checker):
    """Drop table."""

    name = "unsafe.drop_table"
    code = "UST001"

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit DropStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.removeType == enums.ObjectType.OBJECT_TABLE
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Drop table",
                ),
            )


class RenameTable(linter.Checker):
    """Rename table."""

    name = "unsafe.rename_table"
    code = "UST002"

    def visit_RenameStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit RenameStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.renameType == enums.ObjectType.OBJECT_TABLE
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Rename table",
                ),
            )


class TableMovementToTablespace(linter.Checker):
    """Table movement to tablespace."""

    name = "unsafe.table_movement_to_tablespace"
    code = "UST003"

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors[statement_index].stmt.objtype == enums.ObjectType.OBJECT_TABLE
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Table movement to tablespace",
                ),
            )


class TablesMovementToTablespace(linter.Checker):
    """Tables movement to tablespace."""

    name = "unsafe.tables_movement_to_tablespace"
    code = "UST004"

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.objtype == enums.ObjectType.OBJECT_TABLE
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Tables movement to tablespace",
                ),
            )


class Cluster(linter.Checker):
    """Cluster."""

    name = "unsafe.cluster"
    code = "UST005"

    def visit_ClusterStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,  # noqa: ARG002
    ) -> None:
        """Visit ClusterStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ancestors[statement_index].stmt_location,
            self.code,
        ) not in self.ignore_rules:

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Cluster",
                ),
            )


class VacuumFull(linter.Checker):
    """Vacuum full."""

    name = "unsafe.vacuum_full"
    code = "UST006"

    def visit_VacuumStmt(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit VacuumStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        options = (
            [stream.RawStream()(option).lower() for option in node.options]
            if node.options is not None
            else []
        )

        if (
            "full" in options
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Vacuum full",
                ),
            )


class NonConcurrentDetachPartition(linter.Checker):
    """Detach partition."""

    name = "unsafe.detach_partition"
    code = "UST007"

    def visit_PartitionCmd(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit PartitionCmd."""
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
                    description="Non concurrent detach partition",
                ),
            )


class NonConcurrentRefreshMaterializedView(linter.Checker):  # type: ignore[misc]
    """Non concurrent refresh materialized view."""

    name = "unsafe.non_concurrent_refresh_materialized_view"
    code = "UST008"

    def visit_RefreshMatViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit RefreshMatViewStmt."""
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
                    description="Non concurrent refresh materialized view",
                ),
            )
