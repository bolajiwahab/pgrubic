"""Rules for Unsafe migrations."""

from pglast import ast, enums, stream  # type: ignore[import-untyped]

from pgshield import utils, linter


class NonConcurrentIndexCreation(linter.Checker):  # type: ignore[misc]
    """Non concurrent index creation."""

    name = "unsafe.non_concurrent_index_creation"
    code = "UNS001"

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit IndexStmt."""
        if not node.concurrent:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent index creation",
                ),
            )


class ValidatedForeignKeyConstraintOnExistingRows(linter.Checker):  # type: ignore[misc]
    """Validated foreign key constraint on existing rows."""

    name = "unsafe.validated_foreign_key_constraint_on_existing_rows"
    code = "UNS002"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_FOREIGN
            and not node.skip_validation
        ):

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Validated foreign key constraint on existing rows",
                ),
            )


class ValidatedCheckConstraintOnExistingRows(linter.Checker):  # type: ignore[misc]
    """Validated check constraint on existing rows."""

    name = "unsafe.validated_check_constraint_on_existing_rows"
    code = "UNS003"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_CHECK
            and not node.skip_validation
        ):

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Validated check constraint on existing rows",
                ),
            )


class UniqueConstraintCreatingNewIndex(linter.Checker):  # type: ignore[misc]
    """Unique constraint creating new index."""

    name = "unsafe.unique_constraint_creating_new_index"
    code = "UNS004"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_UNIQUE
            and not node.indexname
        ):

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Unique constraint creating new index",
                ),
            )


class PrimaryKeyConstraintCreatingNewIndex(linter.Checker):  # type: ignore[misc]
    """Primary key constraint creating new index."""

    name = "unsafe.primary_key_constraint_creating_new_index"
    code = "UNS005"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_PRIMARY
            and not node.indexname
        ):

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Primary key constraint creating new index",
                ),
            )


class NotNullOnExistingColumn(linter.Checker):  # type: ignore[misc]
    """Not null on existing column."""

    name = "unsafe.not_null_on_existing_column"
    code = "UNS006"

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_SetNotNull:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Not null on existing column",
                ),
            )


class NotNullOnNewColumnWithNoStaticDefault(linter.Checker):  # type: ignore[misc]
    """Not null on new column with no static default."""

    name = "unsafe.not_null_on_new_column_with_no_static_default"
    code = "UNS007"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        if ast.AlterTableStmt in ancestors and node.constraints:

            is_not_null = False
            has_default = False

            for constraint in node.constraints:

                if constraint.contype == enums.ConstrType.CONSTR_NOTNULL:
                    is_not_null = True

                if (
                    constraint.contype == enums.ConstrType.CONSTR_DEFAULT
                    and isinstance(constraint.raw_expr, ast.A_Const)
                ):
                    has_default = True

            if is_not_null and not has_default:

                statement_index: int = utils.get_statement_index(ancestors)

                self.violations.append(
                    linter.Violation(
                        location=ancestors[statement_index].stmt_location,
                        statement=ancestors[statement_index],
                        description="Not null on new column with no static default",
                    ),
                )


class VolatileDefaultOnNewColumn(linter.Checker):  # type: ignore[misc]
    """Volatile default on new column."""

    name = "unsafe.volatile_default_on_new_column"
    code = "UNS008"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_DEFAULT
            and not isinstance(node.raw_expr, ast.A_Const)
        ):

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Volatile default on new column",
                ),
            )


class TableMovementToTablespace(linter.Checker):
    """Table movement to tablespace."""

    name = "unsafe.table_movement_to_tablespace"
    code = "UNS009"

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors[statement_index].stmt.objtype == enums.ObjectType.OBJECT_TABLE
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
    code = "UNS010"

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        if node.objtype == enums.ObjectType.OBJECT_TABLE:

            statement_index: int = utils.get_statement_index(ancestors)

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
    code = "UNS011"

    def visit_ClUNSterStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,  # noqa: ARG002
    ) -> None:
        """Visit ClUNSterStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

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
    code = "UNS012"

    def visit_VacuumStmt(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit VacuumStmt."""
        options = (
            [stream.RawStream()(option) for option in node.options]
            if node.options is not None
            else []
        )

        if "full" in options:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Vacuum full",
                ),
            )


class NonConcurrentRefreshMaterializedView(linter.Checker):  # type: ignore[misc]
    """Non concurrent refresh materialized view."""

    name = "unsafe.non_concurrent_refresh_materialized_view"
    code = "UNS013"

    def visit_RefreshMatViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit RefreshMatViewStmt."""
        if not node.concurrent:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent refresh materialized view",
                ),
            )


class NonConcurrentReindex(linter.Checker):
    """Non concurrent reindex."""

    name = "unsafe.non_concurrent_reindex"
    code = "UNS014"

    def visit_ReindexStmt(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit ReindexStmt."""
        params = (
            [stream.RawStream()(param) for param in node.params]
            if node.params is not None
            else []
        )

        if "concurrently" not in params:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent reindex",
                ),
            )


class DropColumn(linter.Checker):  # type: ignore[misc]
    """Drop column."""

    name = "unsafe.drop_column"
    code = "UNS015"

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_DropColumn:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Drop column",
                ),
            )


class ChangeColumnType(linter.Checker):
    """Change column type."""

    name = "unsafe.change_column_type"
    code = "UNS016"

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_AlterColumnType:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Change column type",
                ),
            )


class RenameColumn(linter.Checker):
    """Rename column."""

    name = "unsafe.rename_column"
    code = "UNS017"

    def visit_RenameStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit RenameStmt."""
        if node.renameType == enums.ObjectType.OBJECT_COLUMN:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Rename column",
                ),
            )


class RenameTable(linter.Checker):
    """Rename table."""

    name = "unsafe.rename_table"
    code = "UNS018"

    def visit_RenameStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit RenameStmt."""
        if node.renameType == enums.ObjectType.OBJECT_TABLE:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Rename table",
                ),
            )


class AutoIncrementColumn(linter.Checker):
    """Auto increment column."""

    name = "unsafe.auto_increment_column"
    code = "UNS019"

    def visit_ColumnDef(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            data_types = (
                [stream.RawStream()(data_type) for data_type in node.typeName.names]
                if node.typeName.names is not None
                else []
            )

            if any(dt in ["'bigserial'", "'serial'"] for dt in data_types):

                self.violations.append(
                    linter.Violation(
                        location=ancestors[statement_index].stmt_location,
                        statement=ancestors[statement_index],
                        description="Auto increment column",
                    ),
                )


class AutoIncrementIdentityColumn(linter.Checker):  # type: ignore[misc]
    """Auto increment identity column."""

    name = "unsafe.auto_increment_identity_column"
    code = "UNS020"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_IDENTITY
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Auto increment identity column",
                ),
            )


class StoredGeneratedColumn(linter.Checker):  # type: ignore[misc]
    """Stored generated column."""

    name = "unsafe.stored_generated_column"
    code = "UNS021"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_GENERATED
        ):

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Stored generated column",
                ),
            )


class IndexMovementToTablespace(linter.Checker):
    """Index movement to tablespace."""

    name = "unsafe.index_movement_to_tablespace"
    code = "UNS022"

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_SetTableSpace
            and ancestors[statement_index].stmt.objtype == enums.ObjectType.OBJECT_INDEX
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
    code = "UNS023"

    def visit_AlterTableMoveAllStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableMoveAllStmt."""
        if node.objtype == enums.ObjectType.OBJECT_INDEX:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Indexes movement to tablespace",
                ),
            )


class DropTable(linter.Checker):
    """Drop table."""

    name = "unsafe.drop_table"
    code = "UNS024"

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_TABLE:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Drop table",
                ),
            )


class NonConcurrentIndexDrop(linter.Checker):
    """Non concurrent index drop."""

    name = "unsafe.non_concurrent_index_drop"
    code = "UNS025"

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_INDEX and not node.concurrent:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent index drop",
                ),
            )


class DropTablespace(linter.Checker):
    """Drop tablespace."""

    name = "unsafe.drop_tablespace"
    code = "UNS026"

    def visit_DropTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit DropTableSpaceStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                location=ancestors[statement_index].stmt_location,
                statement=ancestors[statement_index],
                description="Drop tablespace",
            ),
        )


class DropDatabase(linter.Checker):
    """Drop database."""

    name = "unsafe.drop_database"
    code = "UNS026"

    def visit_DropdbStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit DropdbStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                location=ancestors[statement_index].stmt_location,
                statement=ancestors[statement_index],
                description="Drop database",
            ),
        )
