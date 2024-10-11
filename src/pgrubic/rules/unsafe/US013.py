"""Validating check constraint on existing rows."""

from pglast import ast, enums, visitors

from pgrubic.core import linter


class ValidatingCheckConstraintOnExistingRows(linter.BaseChecker):
    """Validating check constraint on existing rows."""

    is_auto_fixable: bool = True

    def visit_Constraint(
        self,
        ancestors: visitors.Ancestor,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if (
            ancestors.find_nearest(ast.AlterTableCmd)
            and node.contype == enums.ConstrType.CONSTR_CHECK
            and not node.skip_validation
        ):
            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Validating check constraint on existing rows",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.Constraint) -> None:
        """Fix violation."""
        node.skip_validation = True
