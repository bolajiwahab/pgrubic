"""Checker for inline sql function body with wrong language."""

import typing

from pglast import ast, visitors

from pgrubic.core import linter


class InlineSqlFunctionBodyWrongLanguage(linter.BaseChecker):
    """## **What it does**
    Checks for inline sql function bodies which are not defined with LANGUAGE SQL.

    ## **Why not?**
    Inline SQL function bodies are only valid for language SQL.
    While PostgreSQL parses such functions, they fail at creation with the error below:

    ```bash
    ERROR:  inline SQL function body only valid for language SQL
    ```

    ## **When should you?**
    Never.

    ## **Use instead:**
    LANGUAGE SQL.
    """

    is_auto_fixable: bool = True

    def visit_CreateFunctionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        options = typing.cast(tuple[ast.DefElem, ...], node.options)
        language: str | None = None

        for option in options:
            defname = typing.cast(str, option.defname)
            if defname.upper() == "LANGUAGE":
                argument = typing.cast(ast.String, option.arg)
                language = typing.cast(str, argument.sval)
                break

        if node.sql_body and language and language.upper() != "SQL":
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description="Inline SQL function body is only valid for language SQL",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="Use LANGUAGE SQL",
                ),
            )

            self._fix(node)

    def _fix(self, node: ast.CreateFunctionStmt) -> None:
        """Fix violation."""
        options = typing.cast(tuple[ast.DefElem, ...], node.options)

        for option in options:
            defname = typing.cast(str, option.defname)
            argument = typing.cast(ast.String, option.arg)
            if defname.upper() == "LANGUAGE":
                argument.sval = "SQL"
