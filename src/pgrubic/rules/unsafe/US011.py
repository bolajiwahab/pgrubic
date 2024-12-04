"""Checker for not null constraint on new column with volatile default."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NotNullConstraintOnNewColumnWithVolatileDefault(linter.BaseChecker):
    """Not null constraint on new column with volatile default."""

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ancestors.find_nearest(ast.AlterTableCmd) and node.constraints:
            is_not_null = False
            has_static_default = False

            for constraint in node.constraints:
                if constraint.contype == enums.ConstrType.CONSTR_NOTNULL:
                    is_not_null = True

                if constraint.contype == enums.ConstrType.CONSTR_DEFAULT and isinstance(
                    constraint.raw_expr,
                    ast.A_Const,
                ):
                    has_static_default = True

            if is_not_null and not has_static_default:
                self.violations.add(
                    linter.Violation(
                        rule=self.code,
                        line_number=self.line_number,
                        column_offset=self.column_offset,
                        line=self.line,
                        statement_location=self.statement_location,
                        description="Not null constraint on new column with volatile default",  # noqa: E501
                    ),
                )
