"""Checker for not null constraint on existing column."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class NotNullConstraintOnExistingColumn(linter.BaseChecker):
    """Not null constraint on existing column."""

    is_auto_fixable: bool = False

    def visit_AlterTableCmd(
        self,
        ancestors: visitors.Ancestor,
        node: ast.AlterTableCmd,
    ) -> None:
        """Visit AlterTableCmd."""
        if node.subtype == enums.AlterTableType.AT_SetNotNull:

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description=f"Not null constraint on existing column `{node.name}`",
                ),
            )
