"""Checker for duplicate bodies in functions and procedures."""

from pglast import ast, visitors

from pgrubic.core import linter


class DuplicateBody(linter.BaseChecker):
    """## **What it does**
    Checks functions and procedures that specify both an AS clause and an
    SQL-standard body.

    ## **Why not?**
    PostgreSQL rejects declarations with both body forms, regardless of their language
    or contents.

    ## **When should you?**
    Never.

    ## **Use instead:**
    Specify only the intended body, using either an AS clause or an SQL-standard body.
    """

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        if node.sql_body is None or not any(
            option.defname == "as" for option in node.options or ()
        ):
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
                description="Duplicate body",
                is_auto_fixable=self.is_auto_fixable,
                is_fix_enabled=self.is_fix_enabled,
                help="Specify only one body",
            ),
        )
