"""Checker for adding of auto increment column."""

from pglast import ast, visitors

from pgrubic.core import linter


class AddingAutoIncrementColumn(linter.BaseChecker):
    """Adding auto increment column."""

    def visit_ColumnDef(
        self,
        ancestors: visitors.Ancestor,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ancestors.find_nearest(ast.AlterTableCmd) and (
            node.typeName.names[-1].sval in ["smallserial", "serial", "bigserial"]
        ):
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Forbid adding auto increment column",
                ),
            )
