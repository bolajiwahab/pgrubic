"""Rules for Unsafe migrations."""

import typing

from pglast import ast, enums, visitors  # type: ignore[import-untyped]

from pgshield import errors


class EnsureConcurrentIndex(visitors.Visitor):  # type: ignore[misc]
    """Index should be built concurrently."""

    def visit_IndexStmt(
        self,
        ancestors: typing.Any,  # noqa: ARG002, ANN401
        node: ast.Node,
    ) -> None:
        """Visit Index Statement."""
        if not node.concurrent:
            raise errors.IndexNotConcurrentError


class EnsureForeignKeyConstraintNotValidatingExistingRows(visitors.Visitor):  # type: ignore[misc]
    """Foreign key constraint should not validate existing rows in the same transaction."""  # noqa: E501

    def visit_Constraint(
        self,
        ancestors: typing.Any,  # noqa: ANN401
        node: ast.Node,
    ) -> None:
        """Visit Constraint Definition."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_FOREIGN
            and not node.skip_validation
        ):
            raise errors.ForeignKeyConstraintShouldNotValidateExistingRowsError


class EnsureCheckConstraintNotValidatingExistingRows(visitors.Visitor):  # type: ignore[misc]
    """Check constraint should not validate existing rows in the same transaction."""

    def visit_Constraint(
        self,
        ancestors: typing.Any,  # noqa: ANN401
        node: ast.Node,
    ) -> None:
        """Visit Constraint Definition."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_CHECK
            and not node.skip_validation
        ):
            raise errors.CheckConstraintShouldNotValidateExistingRowsError


class EnsureUniqueConstraintNotCreatingUniqueIndex(visitors.Visitor):  # type: ignore[misc]
    """Unique constraint should not create unique index in the same transaction."""

    def visit_Constraint(
        self,
        ancestors: typing.Any,  # noqa: ANN401
        node: ast.Node,
    ) -> None:
        """Visit Constraint Definition."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_UNIQUE
            and not node.indexname
        ):
            raise errors.UniqueConstraintShouldNotCreateUniqueIndexError


class EnsureNoNotNullOnExistingColumn(visitors.Visitor):  # type: ignore[misc]
    """Not Null constraint should not be set directly on an existing column."""

    def visit_AlterTableCmd(
        self,
        ancestors: typing.Any,  # noqa: ANN401
        node: ast.Node,
    ) -> None:
        """Visit Alter Table Command."""
        if (
            ast.AlterTableStmt in ancestors
            and node.subtype == enums.AlterTableType.AT_SetNotNull
        ):
            raise errors.UniqueConstraintShouldNotCreateUniqueIndexError


class EnsureNoNotNullNonConstantDefaultOnNewColumn(visitors.Visitor):  # type: ignore[misc]
    """Not null with constant defaults are safe for new columns."""

    def visit_ColumnDef(
        self,
        ancestors: typing.Any,  # noqa: ANN401
        node: ast.Node,
    ) -> None:
        """Visit Column Definition."""
        if ast.AlterTableStmt in ancestors:
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
                raise errors.UniqueConstraintShouldNotCreateUniqueIndexError


class EnsureConstantDefaultForNewColumn(visitors.Visitor):  # type: ignore[misc]
    """Constants are safe for default for new columns."""

    def visit_Constraint(
        self,
        ancestors: typing.Any,  # noqa: ANN401
        node: ast.Node,
    ) -> None:
        """Visit Constraint Definition."""
        if (
            ast.AlterTableStmt in ancestors
            and node.contype == enums.ConstrType.CONSTR_DEFAULT
            and not isinstance(node.raw_expr, ast.A_Const)
        ):
            raise errors.UniqueConstraintShouldNotCreateUniqueIndexError
