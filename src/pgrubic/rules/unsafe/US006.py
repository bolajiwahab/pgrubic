"""Checker for adding of stored generated column."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class AddingStoredGeneratedColumn(linter.BaseChecker):
    """Adding stored generated column."""

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and node.contype == enums.ConstrType.CONSTR_GENERATED
        ):
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    statement=self.statement,
                    statement_location=self.statement_location,
                    description="Forbid adding stored generated column",
                ),
            )
