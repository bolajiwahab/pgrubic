"""Convention for constraints."""

from pglast import ast, enums

from pgshield.core import linter
from pgshield.core.enums import IdentityConstraintMode


class NotNullColumn(linter.Checker):
    """Not null column."""

    name: str = "convention.not_null_column"
    code: str = "CVR001"

    is_auto_fixable: bool = True

    def _register_violation(
        self,
        column_name: str,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Register the violation."""
        self.violations.append(
            linter.Violation(
                statement_location=statement_location,
                statement_length=statement_length,
                node_location=node_location,
                description=f"Column '{column_name}' is required as not nullable",
            ),
        )

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ast.CreateStmt in ancestors and node.colname in self.config.not_null_columns:

            is_not_null = bool(
                (
                    [
                        constraint
                        for constraint in node.constraints
                        if constraint.contype == enums.ConstrType.CONSTR_NOTNULL
                    ]
                    if node.constraints is not None
                    else []
                ),
            )

            if not is_not_null:

                self._register_violation(
                    column_name=node.colname,
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                )

                if self.config.fix is True:

                    node.constraints = (
                        *(node.constraints or []),
                        ast.Constraint(
                            contype=enums.ConstrType.CONSTR_NOTNULL,
                        ),
                    )

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if (
            node.subtype == enums.AlterTableType.AT_DropNotNull
            and node.name in self.config.not_null_columns
        ):

            self._register_violation(
                column_name=node.name,
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
            )

            if self.config.fix is True and self.config.unsafe_fixes is True:

                node.subtype = enums.AlterTableType.AT_SetNotNull


class PreferNoCascadeDelete(linter.Checker):
    """Prefer no cascade delete."""

    name: str = "convention.prefer_no_cascade_delete"
    code: str = "CVR002"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_FOREIGN
            and node.fk_del_action == enums.FKCONSTR_ACTION_CASCADE
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer no cascade delete",
                ),
            )


class PreferNoCascadeUpdate(linter.Checker):
    """Prefer no cascade update."""

    name: str = "convention.prefer_no_cascade_update"
    code: str = "CVR003"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_FOREIGN
            and node.fk_upd_action == enums.FKCONSTR_ACTION_CASCADE
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer no cascade update",
                ),
            )


class PreferGeneratedAlwaysOverGeneratedByDefaultIdentity(linter.Checker):
    """Prefer generated always over generated by default identity."""

    name = "convention.prefer_generated_always_over_generated_by_default_identity"
    code = "CVR004"

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            node.contype == enums.ConstrType.CONSTR_IDENTITY
            and node.generated_when == IdentityConstraintMode.IDENTITY_BY_DEFAULT
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer generated always over generated by default identity",  # noqa: E501
                ),
            )
