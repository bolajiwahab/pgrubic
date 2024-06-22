"""Unsafe table operations."""

from pglast import ast, enums, stream

from pgshield.core import linter


class DropTable(linter.Checker):
    """Drop table."""

    name = "unsafe.drop_table"
    code = "UST001"

    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.removeType == enums.ObjectType.OBJECT_TABLE:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Drop table",
                ),
            )


class RenameTable(linter.Checker):
    """Rename table."""

    name = "unsafe.rename_table"
    code = "UST002"

    is_auto_fixable: bool = False

    def visit_RenameStmt(
        self,
        ancestors: ast.Node,
        node: ast.RenameStmt,
    ) -> None:
        """Visit RenameStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.renameType == enums.ObjectType.OBJECT_TABLE:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Rename table",
                ),
            )


class TableMovementToTablespace(linter.Checker):
    """Table movement to tablespace."""

    name = "unsafe.table_movement_to_tablespace"
    code = "UST003"

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.AlterTableCmd) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors[statement_index].stmt.objtype == enums.ObjectType.OBJECT_TABLE
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Table movement to tablespace",
                ),
            )


class TablesMovementToTablespace(linter.Checker):
    """Tables movement to tablespace."""

    name = "unsafe.tables_movement_to_tablespace"
    code = "UST004"

    is_auto_fixable: bool = False

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableMoveAllStmt,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.objtype == enums.ObjectType.OBJECT_TABLE:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Tables movement to tablespace",
                ),
            )


class Cluster(linter.Checker):
    """Cluster."""

    name = "unsafe.cluster"
    code = "UST005"

    is_auto_fixable: bool = False

    def visit_ClusterStmt(
        self,
        ancestors: ast.Node,
        node: ast.ClusterStmt,
    ) -> None:
        """Visit ClusterStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=ancestors[statement_index].stmt_location,
                column_offset=linter.get_column_offset(ancestors, node),
                statement=ancestors[statement_index],
                description="Cluster",
            ),
        )


class VacuumFull(linter.Checker):
    """Vacuum full."""

    name = "unsafe.vacuum_full"
    code = "UST006"

    is_auto_fixable: bool = False

    def visit_VacuumStmt(self, ancestors: ast.Node, node: ast.VacuumStmt) -> None:
        """Visit VacuumStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        options = (
            [stream.RawStream()(option) for option in node.options]
            if node.options is not None
            else []
        )

        if options and "full" in options:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Vacuum full",
                ),
            )


class NonConcurrentDetachPartition(linter.Checker):
    """Detach partition."""

    name = "unsafe.detach_partition"
    code = "UST007"

    is_auto_fixable: bool = False

    def visit_PartitionCmd(
        self,
        ancestors: ast.Node,
        node: ast.PartitionCmd,
    ) -> None:
        """Visit PartitionCmd."""
        statement_index: int = linter.get_statement_index(ancestors)

        if not node.concurrent:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Non concurrent detach partition",
                ),
            )


class NonConcurrentRefreshMaterializedView(linter.Checker):
    """Non concurrent refresh materialized view."""

    name = "unsafe.non_concurrent_refresh_materialized_view"
    code = "UST008"

    is_auto_fixable: bool = False

    def visit_RefreshMatViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.RefreshMatViewStmt,
    ) -> None:
        """Visit RefreshMatViewStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if not node.concurrent:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Non concurrent refresh materialized view",
                ),
            )


class TruncateTable(linter.Checker):
    """Truncate table."""

    name = "unsafe.truncate_table"
    code = "UNT009"

    is_auto_fixable: bool = False

    def visit_TruncateStmt(
        self,
        ancestors: ast.Node,
        node: ast.TruncateStmt,
    ) -> None:
        """Visit TruncateStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=ancestors[statement_index].stmt_location,
                column_offset=linter.get_column_offset(ancestors, node),
                statement=ancestors[statement_index],
                description="Truncate table is not safe",
            ),
        )
