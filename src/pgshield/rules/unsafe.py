"""Rules for Unsafe migrations."""

from pglast import ast, enums, stream  # type: ignore[import-untyped]

from pgshield import utils, linter


class NonConcurrentIndexCreation(linter.Checker):  # type: ignore[misc]
    """Non concurrent index creation."""

    name = "unsafe.non_concurrent_index_creation"
    code = "US001"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent index creation",
                ),
            )


class ValidatedForeignKeyConstraintOnExistingRows(linter.Checker):  # type: ignore[misc]
    """Validated foreign key constraint on existing rows."""

    name = "unsafe.validated_foreign_key_constraint_on_existing_rows"
    code = "US002"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Validated foreign key constraint on existing rows",
                ),
            )


class ValidatedCheckConstraintOnExistingRows(linter.Checker):  # type: ignore[misc]
    """Validated check constraint on existing rows."""

    name = "unsafe.validated_check_constraint_on_existing_rows"
    code = "US003"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Validated check constraint on existing rows",
                ),
            )


class UniqueConstraintCreatingNewIndex(linter.Checker):  # type: ignore[misc]
    """Unique constraint creating new index."""

    name = "unsafe.unique_constraint_creating_new_index"
    code = "US004"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Unique constraint creating new index",
                ),
            )


class PrimaryKeyConstraintCreatingNewIndex(linter.Checker):  # type: ignore[misc]
    """Primary key constraint creating new index."""

    name = "unsafe.primary_key_constraint_creating_new_index"
    code = "US005"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Primary key constraint creating new index",
                ),
            )


class NotNullOnExistingColumn(linter.Checker):  # type: ignore[misc]
    """Not null on existing column."""

    name = "unsafe.not_null_on_existing_column"
    code = "US006"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Not null on existing column",
                ),
            )


class NotNullOnNewColumnWithNoStaticDefault(linter.Checker):  # type: ignore[misc]
    """Not null on new column with no static default."""

    name = "unsafe.not_null_on_new_column_with_no_static_default"
    code = "US007"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                        description="Not null on new column with no static default",
                    ),
                )


class VolatileDefaultOnNewColumn(linter.Checker):  # type: ignore[misc]
    """Volatile default on new column."""

    name = "unsafe.volatile_default_on_new_column"
    code = "US008"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Volatile default on new column",
                ),
            )


class TableMoveToTablespace(linter.Checker):
    """Table movement to tablespace."""

    name = "unsafe.table_move_to_tablespace"
    code = "US009"

    def visit_AlterTableCmd(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_SetTableSpace:

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Table movement to tablespace",
                ),
            )


class TablesMovementToTablespace(linter.Checker):
    """Tables movement to tablespace."""

    name = "unsafe.tables_movement_to_tablespace"
    code = "US010"

    def visit_AlterTableMoveAllStmt(self, ancestors: ast.Node, node: ast.Node) -> None:  # noqa: ARG002
        """Visit AlterTableMoveAllStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=ancestors[statement_index].stmt_location,
                statement=ancestors[statement_index],
                description="Tables movement to tablespace",
            ),
        )


class Cluster(linter.Checker):
    """Cluster."""

    name = "unsafe.cluster"
    code = "US0011"

    def visit_ClusterStmt(self, ancestors: ast.Node, node: ast.Node) -> None:  # noqa: ARG002
        """Visit ClusterStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=ancestors[statement_index].stmt_location,
                statement=ancestors[statement_index],
                description="Cluster",
            ),
        )


class VacuumFull(linter.Checker):
    """Vacuum full."""

    name = "unsafe.vacuum_full"
    code = "US0012"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Vacuum full",
                ),
            )


class NonConcurrentRefreshMaterializedView(linter.Checker):  # type: ignore[misc]
    """Non concurrent refresh materialized view."""

    name = "unsafe.non_concurrent_refresh_materialized_view"
    code = "US013"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent refresh materialized view",
                ),
            )


class NonConcurrentReindex(linter.Checker):
    """Non concurrent reindex."""

    name = "unsafe.non_concurrent_reindex"
    code = "US014"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent reindex",
                ),
            )


class DropColumn(linter.Checker):  # type: ignore[misc]
    """Drop column."""

    name = "unsafe.drop_column"
    code = "US015"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Drop column",
                ),
            )


class ChangeColumnType(linter.Checker):
    """Change column type."""

    name = "unsafe.change_column_type"
    code = "US016"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Change column type",
                ),
            )


class RenameColumn(linter.Checker):
    """Rename column."""

    name = "unsafe.rename_column"
    code = "US017"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Rename column",
                ),
            )


class RenameTable(linter.Checker):
    """Rename table."""

    name = "unsafe.rename_table"
    code = "US018"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Rename table",
                ),
            )


class AutoIncrementColumn(linter.Checker):
    """Auto increment column."""

    name = "unsafe.auto_increment_column"
    code = "US0013"

    def visit_ColumnDef(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit ColumnDef."""
        if ast.AlterTableStmt in ancestors:
            data_types = (
                [stream.RawStream()(data_type) for data_type in node.typeName.names]
                if node.typeName.names is not None
                else []
            )

            if any(dt in ["'bigserial'", "'serial'"] for dt in data_types):

                statement_index: int = utils.get_statement_index(ancestors)

                self.violations.append(
                    linter.Violation(
                        lineno=ancestors[statement_index].stmt_location,
                        statement=ancestors[statement_index],
                        description="Auto increment column",
                    ),
                )

class AutoIncrementIdentityColumn(linter.Checker):  # type: ignore[misc]
    """Auto increment identity column."""

    name = "unsafe.auto_increment_identity_column"
    code = "US0014"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_IDENTITY
        ):

            statement_index: int = utils.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Auto increment identity column",
                ),
            )


class StoredGeneratedColumn(linter.Checker):  # type: ignore[misc]
    """Stored generated column."""

    name = "unsafe.stored_generated_column"
    code = "US0015"

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
                    lineno=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Stored generated column",
                ),
            )
