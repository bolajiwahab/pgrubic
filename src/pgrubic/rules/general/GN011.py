"""Checker for missing required columns."""

from pglast import ast, enums, visitors

from pgrubic.core import config, linter
from pgrubic.rules.general import get_columns_from_table_creation


class MissingRequiredColumn(linter.BaseChecker):
    """## **What it does**
    Checks for missing required column.

    ## **Why not?**
    If a column has been specified as required and you have not defined it,
    you are probably doing something wrong.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Define the required column.

    ## **Configuration**
    `required-columns`: List of required columns along with their data types.
    """

    is_auto_fixable: bool = True

    def visit_CreateStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if not node.partbound and node.tableElts:
            given_columns, _ = get_columns_from_table_creation(node)

            for required_column in self.config.lint.required_columns:
                if not any(
                    required_column.name == column.name for column in given_columns
                ):
                    self.violations.add(
                        linter.Violation(
                            rule_code=self.code,
                            rule_name=self.name,
                            rule_category=self.category,
                            line_number=self.line_number,
                            column_offset=self.column_offset,
                            line=self.line,
                            statement_location=self.statement_location,
                            description=f"Column `{required_column.name}` of type"
                            f" `{required_column.data_type}` is marked as required in config",  # noqa: E501
                            is_auto_fixable=self.is_auto_fixable,
                            is_fix_enabled=self.is_fix_enabled,
                            help="Define the required column",
                        ),
                    )

                    self._fix(node, required_column)

    def _fix(self, node: ast.CreateStmt, column: config.Column) -> None:
        """Fix violation."""
        node.tableElts = (
            *node.tableElts,
            ast.ColumnDef(
                colname=column.name,
                typeName=ast.TypeName(
                    names=(
                        {
                            "@": "String",
                            "sval": column.data_type,
                        },
                    ),
                ),
                constraints=(
                    *(node.constraints or []),
                    ast.Constraint(
                        contype=enums.ConstrType.CONSTR_NOTNULL,
                    ),
                ),
            ),
        )
