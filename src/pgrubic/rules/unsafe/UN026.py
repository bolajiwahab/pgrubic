"""Checker for vacuum full."""

from pglast import ast, visitors

from pgrubic.core import linter


class VacuumFull(linter.BaseChecker):
    """Vacuum full."""

    is_auto_fixable: bool = False

    def visit_VacuumStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.VacuumStmt,
    ) -> None:
        """Visit VacuumStmt."""
        options = [option.defname for option in node.options] if node.options else []

        if "full" in options:

            self.violations.add(
                linter.Violation(
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    source_text=self.source_text,
                    statement_location=self.statement_location,
                    description="Vacuum full found",
                ),
            )
