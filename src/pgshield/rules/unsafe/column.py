"""Unsafe column operations."""

from pglast import ast, enums, stream  # type: ignore[import-untyped]

from pgshield import utils, linter


class DropColumn(linter.Checker):  # type: ignore[misc]
    """Drop column."""

    name = "unsafe.drop_column"
    code = "USC001"

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_DropColumn
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

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
    code = "USC002"

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_AlterColumnType
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

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
    code = "USC003"

    def visit_RenameStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit RenameStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.renameType == enums.ObjectType.OBJECT_COLUMN
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Rename column",
                ),
            )


class AutoIncrementColumn(linter.Checker):
    """Auto increment column."""

    name = "unsafe.auto_increment_column"
    code = "USC004"

    def visit_ColumnDef(self, ancestors: ast.Node, node: ast.Node) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.AlterTableStmt in ancestors:

            # Get data type e.g ["pg_catalog", "bigserial"]
            data_type = [
                stream.RawStream()(data_type).strip("'")
                for data_type in node.typeName.names
            ]

            if (
                data_type[-1] in ["serial", "bigserial"]
                and (ancestors[statement_index].stmt_location, self.code)
                not in self.ignore_rules
            ):

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
    code = "USC005"

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
    code = "USC006"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_GENERATED
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Stored generated column",
                ),
            )
