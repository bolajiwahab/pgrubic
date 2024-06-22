"""Convention for constraints."""

from pglast import ast, enums

from pgshield.core import linter


class NotNullColumn(linter.Checker):
    """Not null column."""

    name: str = "convention.not_null_column"
    code: str = "CVR001"

    is_auto_fixable: bool = True

    def _register_violation(
        self,
        column: str,
        lineno: int,
        column_offset: int,
        statement: str,
    ) -> None:
        """Register the violation."""
        self.violations.append(
            linter.Violation(
                lineno=lineno,
                column_offset=column_offset,
                statement=statement,
                description=f"Column '{column}' is required as not nullable",
            ),
        )

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ast.CreateStmt in ancestors and node.colname in self.config.not_null_columns:

            statement_index: int = linter.get_statement_index(ancestors)

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
                    column=node.colname,
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
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

            statement_index: int = linter.get_statement_index(ancestors)

            self._register_violation(
                column=node.name,
                lineno=ancestors[statement_index].stmt_location,
                column_offset=linter.get_column_offset(ancestors, node),
                statement=ancestors[statement_index],
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

            statement_index: int = linter.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
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

            statement_index: int = linter.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer no cascade update",
                ),
            )
