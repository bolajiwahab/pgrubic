"""Checker for adding of auto increment identity column."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class AddingAutoIncrementIdentityColumn(linter.BaseChecker):
    """Forbid adding auto increment identity column."""

    is_auto_fixable: bool = False

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        alter_table_cmd: visitors.Ancestor = ancestors.find_nearest(ast.AlterTableCmd)

        if (
            alter_table_cmd
            and alter_table_cmd.node.subtype == enums.AlterTableType.AT_AddColumn
            and node.contype == enums.ConstrType.CONSTR_IDENTITY
        ):

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Forbid adding auto increment identity column",
                ),
            )