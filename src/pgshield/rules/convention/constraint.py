"""Convention for constraints."""

from pglast import ast, enums  # type: ignore[import-untyped]

from pgshield.core import linter


class NotNullColumn(linter.Checker):
    """Not null column."""

    name = "convention.not_null_column"
    code = "CVR001"

    def _register_violation(
        self,
        column: str | None,
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
                description=f"Column '{column}' is not nullable",
            ),
        )

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors
        ) and node.colname in self.config.not_null_columns:

            is_not_null = False

            if node.constraints is not None:

                for constraint in node.constraints:

                    if constraint.contype == enums.ConstrType.CONSTR_NOTNULL:

                        is_not_null = True

            if not is_not_null:

                statement_index: int = linter.get_statement_index(ancestors)

                self._register_violation(
                    column=node.colname,
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                )

    def visit_AlterTableCmd(
        self,
        ancestors: ast.Node,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            node.subtype == enums.AlterTableType.AT_DropNotNull
            and node.name in self.config.not_null_columns
        ):

            self._register_violation(
                column=node.name,
                lineno=ancestors[statement_index].stmt_location,
                column_offset=linter.get_column_offset(ancestors, node),
                statement=ancestors[statement_index],
            )


class TableShouldHavePrimaryKey(linter.Checker):
    """Table should have a primary key."""

    name = "convention.table_should_have_primary_key"
    code = "CVR002"

    def _check_for_table_level_primary_key(
        self,
        node: ast.CreateStmt,
    ) -> bool:
        """Check for table level primary key."""
        has_primary_key = False

        for definition in node.tableElts:

            if (
                isinstance(definition, ast.Constraint)
            ) and definition.contype == enums.ConstrType.CONSTR_PRIMARY:

                has_primary_key = True

        return has_primary_key

    def _check_for_column_level_primary_key(
        self,
        node: ast.CreateStmt,
    ) -> bool:
        """Check for column level primary key."""
        has_primary_key = False

        for definition in node.tableElts:

            if isinstance(definition, ast.ColumnDef) and definition.constraints:

                for constraint in definition.constraints:

                    if constraint.contype == enums.ConstrType.CONSTR_PRIMARY:

                        has_primary_key = True

        return has_primary_key

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
                    description="Table should have a primary key",
                ),
            )
