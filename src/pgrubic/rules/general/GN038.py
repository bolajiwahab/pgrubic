"""Checker for missing languages in functions and procedures."""

from pglast import ast, visitors

from pgrubic import postgres
from pgrubic.core import linter


class MissingLanguage(linter.BaseChecker):
    """## **What it does**
    Checks functions and procedures for a missing language.

    ## **Why not?**
    PostgreSQL requires a language when creating a function or procedure, unless
    an SQL-standard body is supplied. SQL-standard bodies implicitly use LANGUAGE SQL.
    DO statements default to PL/pgSQL and do not require an explicit language.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Specify the language used by the body, or supply an SQL-standard body.
    """

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        if postgres.functions.has_language(node):
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
                description="Missing language",
                is_auto_fixable=self.is_auto_fixable,
                is_fix_enabled=self.is_fix_enabled,
                help="Specify a language",
            ),
        )
