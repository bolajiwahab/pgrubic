"""Unsafe table operations."""

from pglast import ast, enums, stream

from pgshield.core import linter


class DropTable(linter.Checker):
    """Drop table."""

    name: str = "unsafe.drop_table"
    code: str = "UST001"

    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_TABLE:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Drop table",
                ),
            )


class RenameTable(linter.Checker):
    """Rename table."""

    name: str = "unsafe.rename_table"
    code: str = "UST002"

    is_auto_fixable: bool = False

    def visit_RenameStmt(
        self,
        ancestors: ast.Node,
        node: ast.RenameStmt,
    ) -> None:
        """Visit RenameStmt."""
        if node.renameType == enums.ObjectType.OBJECT_TABLE:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Rename table",
                ),
            )


class TableMovementToTablespace(linter.Checker):
    """Table movement to tablespace."""

    name: str = "unsafe.table_movement_to_tablespace"
    code: str = "UST003"

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.AlterTableCmd) -> None:
        """Visit AlterTableCmd."""
        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors[2].stmt.objtype == enums.ObjectType.OBJECT_TABLE
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Table movement to tablespace",
                ),
            )


class TablesMovementToTablespace(linter.Checker):
    """Tables movement to tablespace."""

    name: str = "unsafe.tables_movement_to_tablespace"
    code: str = "UST004"

    is_auto_fixable: bool = False

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableMoveAllStmt,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        if node.objtype == enums.ObjectType.OBJECT_TABLE:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Tables movement to tablespace",
                ),
            )


class Cluster(linter.Checker):
    """Cluster."""

    name: str = "unsafe.cluster"
    code: str = "UST005"

    is_auto_fixable: bool = False

    def visit_ClusterStmt(
        self,
        ancestors: ast.Node,
        node: ast.ClusterStmt,
    ) -> None:
        """Visit ClusterStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Cluster",
            ),
        )


class VacuumFull(linter.Checker):
    """Vacuum full."""

    name: str = "unsafe.vacuum_full"
    code: str = "UST006"

    is_auto_fixable: bool = False

    def visit_VacuumStmt(self, ancestors: ast.Node, node: ast.VacuumStmt) -> None:
        """Visit VacuumStmt."""
        options = (
            [stream.RawStream()(option) for option in node.options]
            if node.options is not None
            else []
        )

        if options and "full" in options:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Vacuum full",
                ),
            )


class NonConcurrentDetachPartition(linter.Checker):
    """Detach partition."""

    name: str = "unsafe.detach_partition"
    code: str = "UST007"

    is_auto_fixable: bool = False

    def visit_PartitionCmd(
        self,
        ancestors: ast.Node,
        node: ast.PartitionCmd,
    ) -> None:
        """Visit PartitionCmd."""
        if not node.concurrent:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent detach partition",
                ),
            )


class NonConcurrentRefreshMaterializedView(linter.Checker):
    """Non concurrent refresh materialized view."""

    name: str = "unsafe.non_concurrent_refresh_materialized_view"
    code: str = "UST008"

    is_auto_fixable: bool = False

    def visit_RefreshMatViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.RefreshMatViewStmt,
    ) -> None:
        """Visit RefreshMatViewStmt."""
        if not node.concurrent:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Non concurrent refresh materialized view",
                ),
            )


class TruncateTable(linter.Checker):
    """Truncate table."""

    name: str = "unsafe.truncate_table"
    code: str = "UNT009"

    is_auto_fixable: bool = False

    def visit_TruncateStmt(
        self,
        ancestors: ast.Node,
        node: ast.TruncateStmt,
    ) -> None:
        """Visit TruncateStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Truncate table is not safe",
            ),
        )


class ForbidUpdateWithoutWhereClause(linter.Checker):
    """Forbid update without where clause."""

    name: str = "unsafe.forbid_update_without_where_clause"
    code: str = "UNT010"

    is_auto_fixable: bool = False

    def visit_UpdateStmt(
        self,
        ancestors: ast.Node,
        node: ast.UpdateStmt,
    ) -> None:
        """Visit UpdateStmt."""
        if node.whereClause is None:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid update without whereclause",
                ),
            )


class ForbidDeleteWithoutWhereClause(linter.Checker):
    """Forbid delete without where clause."""

    name: str = "unsafe.forbid_delete_without_where_clause"
    code: str = "UNT011"

    is_auto_fixable: bool = False

    def visit_DeleteStmt(
        self,
        ancestors: ast.Node,
        node: ast.DeleteStmt,
    ) -> None:
        """Visit DeleteStmt."""
        if node.whereClause is None:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid delete without whereclause",
                ),
            )
