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
            (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors)
            and node.colname in self.config.not_null_columns
            and not node.is_not_null
        ):

            statement_index: int = linter.get_statement_index(ancestors)

            self._register_violation(
                column=node.colname,
                lineno=ancestors[statement_index].stmt_location,
                column_offset=node.location,
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
                column_offset=node.location,
                statement=ancestors[statement_index],
            )
