"""Unsafe column operations."""

from pglast import ast, enums

from pgshield.core import linter


class ForbidDropColumn(linter.Checker):
    """Drop column."""

    name = "unsafe.forbid_drop_column"
    code = "USC001"

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_DropColumn:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid drop column",
                ),
            )


class ForbidColumnTypeChange(linter.Checker):
    """Forbid column type change."""

    name = "unsafe.forbid_column_type_change"
    code = "USC002"

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_AlterColumnType:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid column type change",
                ),
            )


class ForbidColumnRename(linter.Checker):
    """Forbid column rename."""

    name = "unsafe.forbid_column_rename"
    code = "USC003"

    is_auto_fixable: bool = False

    def visit_RenameStmt(
        self,
        ancestors: ast.Node,
        node: ast.RenameStmt,
    ) -> None:
        """Visit RenameStmt."""
        if node.renameType == enums.ObjectType.OBJECT_COLUMN:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid column rename",
                ),
            )


class ForbidAddingAutoIncrementColumn(linter.Checker):
    """Forbid adding auto increment column."""

    name = "unsafe.forbid_adding_auto_increment_column"
    code = "USC004"

    is_auto_fixable: bool = False

    def visit_ColumnDef(self, ancestors: ast.Node, node: ast.ColumnDef) -> None:
        """Visit ColumnDef."""
        if ast.AlterTableStmt in ancestors and (
            node.typeName.names[-1].sval in ["serial", "bigserial"]
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid adding auto increment column",
                ),
            )


class ForbidAddingAutoIncrementIdentityColumn(linter.Checker):
    """Forbid adding auto increment identity column."""

    name = "unsafe.forbid_adding_auto_increment_identity_column"
    code = "USC005"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_IDENTITY
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Forbid adding auto increment identity column",
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
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_GENERATED
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Stored generated column",
                ),
            )
