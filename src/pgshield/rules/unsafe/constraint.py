"""Unsafe constraint operations."""

from pglast import ast, enums

from pgshield.core import linter


class NotNullOnExistingColumn(linter.Checker):
    """Not null on existing column."""

    name = "unsafe.not_null_on_existing_column"
    code = "USR001"

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.subtype == enums.AlterTableType.AT_SetNotNull:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Not null on existing column",
                ),
            )


class NotNullOnNewColumnWithNoStaticDefault(linter.Checker):
    """Not null on new column with no static default."""

    name = "unsafe.not_null_on_new_column_with_no_static_default"
    code = "USR002"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.AlterTableStmt in ancestors and node.constraints:

            is_not_null = False
            has_static_default = False

            for constraint in node.constraints:

                if constraint.contype == enums.ConstrType.CONSTR_NOTNULL:
                    is_not_null = True
                    location = constraint.location

                if (
                    constraint.contype == enums.ConstrType.CONSTR_DEFAULT
                    and isinstance(constraint.raw_expr, ast.A_Const)
                ):
                    has_static_default = True

            if is_not_null and not has_static_default:

                # print(node.location)

                # print(linter.get_column_offset(ancestors, node))
                # print(ancestors.node)
                # print(ancestors.parent)
                # print(abs(ancestors))
                # print(ancestors[statement_index].stmt_location)
                # print(node.location)
                # print(node.constraints)

                self.violations.append(
                    linter.Violation(
                        statement_location=ancestors[statement_index].stmt_location,
                        statement_length=ancestors[statement_index].stmt_len,
                        column_offset=location,
                        description="Not null on new column with no static default",
                    ),
                )


# class VolatileDefaultOnNewColumn(linter.Checker):
#     """Volatile default on new column."""

#     name = "unsafe.volatile_default_on_new_column"
#     code = "USR003"

#     is_auto_fixable: bool = False

#     def visit_Constraint(
#         self,
#         ancestors: ast.Node,
#         node: ast.Constraint,
#     ) -> None:
#         """Visit Constraint."""
#         statement_index: int = linter.get_statement_index(ancestors)

#         if (
#             ast.AlterTableStmt in ancestors
#             and node.contype == enums.ConstrType.CONSTR_DEFAULT
#             and not isinstance(node.raw_expr, ast.A_Const)
#         ):

#             self.violations.append(
#                 linter.Violation(
#                     statement_location=ancestors[statement_index].stmt_location,
#                     statement_length=ancestors[statement_index].stmt_len,
#                     column_offset=linter.get_column_offset(ancestors, node),
#                     description="Volatile default on new column",
#                 ),
#             )


class ValidatedForeignKeyConstraintOnExistingRows(linter.Checker):
    """Validated foreign key constraint on existing rows."""

    name = "unsafe.validated_foreign_key_constraint_on_existing_rows"
    code = "USR004"

    is_auto_fixable = True

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_FOREIGN
            and not node.skip_validation
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Validated foreign key constraint on existing rows",
                ),
            )

            if self.config.fix is True:

                node.skip_validation = True

class ValidatedCheckConstraintOnExistingRows(linter.Checker):
    """Validated check constraint on existing rows."""

    name = "unsafe.validated_check_constraint_on_existing_rows"
    code = "USR005"

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
            and node.contype == enums.ConstrType.CONSTR_CHECK
            and not node.skip_validation
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Validated check constraint on existing rows",
                ),
            )


class UniqueConstraintCreatingNewIndex(linter.Checker):
    """Unique constraint creating new index."""

    name = "unsafe.unique_constraint_creating_new_index"
    code = "USR006"

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
            and node.contype == enums.ConstrType.CONSTR_UNIQUE
            and not node.indexname
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Unique constraint creating new index",
                ),
            )


class PrimaryKeyConstraintCreatingNewIndex(linter.Checker):
    """Primary key constraint creating new index."""

    name = "unsafe.primary_key_constraint_creating_new_index"
    code = "USR007"

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
            and node.contype == enums.ConstrType.CONSTR_PRIMARY
            and not node.indexname
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Primary key constraint creating new index",
                ),
            )
