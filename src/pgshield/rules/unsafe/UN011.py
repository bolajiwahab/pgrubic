"""Unsafe constraint operations."""

from pglast import ast, enums

from pgshield.core import linter


class NotNullOnNewColumnWithNoStaticDefault(linter.Checker):
    """Not null on new column with no static default."""

    name: str = "unsafe.not_null_on_new_column_with_no_static_default"
    code: str = "USR002"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ast.AlterTableStmt in ancestors and node.constraints:

            is_not_null = False
            has_static_default = False

            for constraint in node.constraints:

                if constraint.contype == enums.ConstrType.CONSTR_NOTNULL:
                    is_not_null = True

                if (
                    constraint.contype == enums.ConstrType.CONSTR_DEFAULT
                    and isinstance(constraint.raw_expr, ast.A_Const)
                ):
                    has_static_default = True

            if is_not_null and not has_static_default:

                self.violations.append(
                    linter.Violation(
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                        description="Not null on new column with no static default",
                    ),
                )
