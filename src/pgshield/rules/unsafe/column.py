"""Unsafe column operations."""

from pglast import ast, enums

from pgshield.core import linter


class DropColumn(linter.Checker):
    """Drop column."""

    name = "unsafe.drop_column"
    code = "USC001"

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.subtype == enums.AlterTableType.AT_DropColumn:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Drop column",
                ),
            )


class ChangeColumnType(linter.Checker):
    """Change column type."""

    name = "unsafe.change_column_type"
    code = "USC002"

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.subtype == enums.AlterTableType.AT_AlterColumnType:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Change column type",
                ),
            )


class RenameColumn(linter.Checker):
    """Rename column."""

    name = "unsafe.rename_column"
    code = "USC003"

    is_auto_fixable: bool = False

    def visit_RenameStmt(
        self,
        ancestors: ast.Node,
        node: ast.RenameStmt,
    ) -> None:
        """Visit RenameStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.renameType == enums.ObjectType.OBJECT_COLUMN:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Rename column",
                ),
            )


class AutoIncrementColumn(linter.Checker):
    """Auto increment column."""

    name = "unsafe.auto_increment_column"
    code = "USC004"

    is_auto_fixable: bool = False

    def visit_ColumnDef(self, ancestors: ast.Node, node: ast.ColumnDef) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.AlterTableStmt in ancestors and (
            node.typeName.names[-1].sval in ["serial", "bigserial"]
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Auto increment column",
                ),
            )


class AutoIncrementIdentityColumn(linter.Checker):
    """Auto increment identity column."""

    name = "unsafe.auto_increment_identity_column"
    code = "USC005"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_IDENTITY
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Auto increment identity column",
                ),
            )


class StoredGeneratedColumn(linter.Checker):
    """Stored generated column."""

    name = "unsafe.stored_generated_column"
    code = "USC006"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_GENERATED
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Stored generated column",
                ),
            )
