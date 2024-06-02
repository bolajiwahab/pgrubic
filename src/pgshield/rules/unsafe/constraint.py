"""Unsafe constraint operations."""

from pglast import ast, enums  # type: ignore[import-untyped]

from pgshield import utils, linter


class NotNullOnExistingColumn(linter.Checker):  # type: ignore[misc]
    """Not null on existing column."""

    name = "unsafe.not_null_on_existing_column"
    code = "USR001"

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_SetNotNull
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

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
    code = "USR002"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

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

            if (
                is_not_null
                and not has_default
                and (ancestors[statement_index].stmt_location, self.code)
                not in self.ignore_rules
            ):

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
    code = "USR003"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_DEFAULT
            and not isinstance(node.raw_expr, ast.A_Const)
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Volatile default on new column",
                ),
            )


class ValidatedForeignKeyConstraintOnExistingRows(linter.Checker):  # type: ignore[misc]
    """Validated foreign key constraint on existing rows."""

    name = "unsafe.validated_foreign_key_constraint_on_existing_rows"
    code = "USR004"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_FOREIGN
            and not node.skip_validation
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

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
    code = "USR005"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_CHECK
            and not node.skip_validation
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

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
    code = "USR006"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_UNIQUE
            and not node.indexname
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

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
    code = "USR007"

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_PRIMARY
            and not node.indexname
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Primary key constraint creating new index",
                ),
            )
