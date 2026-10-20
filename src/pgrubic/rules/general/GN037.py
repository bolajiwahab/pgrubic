"""Checker for missing bodies in functions, procedures, and DO statements."""

from pglast import ast, visitors

from pgrubic import postgres
from pgrubic.core import linter


class MissingBody(linter.BaseChecker):
    """## **What it does**
    Checks functions, procedures, and DO statements for missing bodies.

    ## **Why not?**
    PostgreSQL requires a body to create a function or procedure, or execute a
    DO statement.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Specify a body.
    """

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        self._check_body(node)

    def visit_DoStmt(self, ancestors: visitors.Ancestor, node: ast.DoStmt) -> None:
        """Visit DoStmt."""
        self._check_body(node)

    def _check_body(self, node: ast.CreateFunctionStmt | ast.DoStmt) -> None:
        """Report a missing body."""
        if postgres.functions.has_body(node):
            return

        self.violations.add(
            linter.Violation(
                rule_code=self.code,
                rule_name=self.name,
                rule_category=self.category,
                line_number=self.line_number,
                column_offset=self.column_offset,
                line=self.line,
                statement_location=self.statement_location,
                description="Missing body",
                is_auto_fixable=self.is_auto_fixable,
                is_fix_enabled=self.is_fix_enabled,
                help="Specify a body",
            ),
        )
