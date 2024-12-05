"""Checker for adding of auto increment column."""

from pglast import ast, visitors

from pgrubic.core import linter


class AddingAutoIncrementColumn(linter.BaseChecker):
    """## **What it does**
    Checks for adding of auto increment column.

    ## **Why is this bad?**

    Adding auto increment column is not safe.
    """

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
                    rule=self.code,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Adding auto increment column is not safe",
                    auto_fixable=self.is_auto_fixable,
                ),
            )
