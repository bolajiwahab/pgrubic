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


class TableShouldHavePrimaryKey(linter.Checker):
    """Table should have a primary key."""

    name: str = "convention.table_should_have_primary_key"
    code: str = "CVR002"

    is_auto_fixable: bool = False

    def _check_for_table_level_primary_key(
        self,
        node: ast.CreateStmt,
    ) -> bool:
        """Check for table level primary key."""
        return bool(
            (
                [
                    definition
                    for definition in node.tableElts
                    if isinstance(definition, ast.Constraint)
                    and definition.contype == enums.ConstrType.CONSTR_PRIMARY
                ]
            ),
        )

    def _check_for_column_level_primary_key(
        self,
        node: ast.CreateStmt,
    ) -> bool:
        """Check for column level primary key."""
        return bool(
            (
                [
                    definition
                    for definition in node.tableElts
                    if isinstance(definition, ast.ColumnDef) and definition.constraints
                    for constraint in definition.constraints
                    if constraint.contype == enums.ConstrType.CONSTR_PRIMARY
                ]
            ),
        )

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            node.tableElts
            and not self._check_for_column_level_primary_key(node)
            and not self._check_for_table_level_primary_key(node)
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description=f"Table {node.relation.relname} should have a primary key",  # noqa: E501
                ),
            )
