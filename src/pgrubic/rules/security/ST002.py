"""Convention for extensions."""

from pglast import ast, visitors

from pgrubic.core import linter


class ProceduralLanguageWhitelist(linter.BaseChecker):
    """## **What it does**
    Checks that a procedural language to be created is allowed.

    ## **Why not?**
    By default, any procedural language can be loaded into the database.
    This is quite dangerous as some unsafe operations might be introduced by languages.
    So you not only want to empower **CREATE LANGUAGE** to database owners, you
    also want to be able to review and explicitly allow procedural languages.

    ## **When should you?**
    Almost never. If a procedural language is not allowed, you are probably doing
    something wrong.

    ## **Use instead:**
    Procedural languages that are allowed.

    ## **Configuration**
    `allowed-languages`: List of allowed languages.
    """

    def visit_CreatePLangStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreatePLangStmt,
    ) -> None:
        """Visit CreatePLangStmt."""
        if (
            node.plname not in self.config.lint.allowed_languages
            and "*" not in self.config.lint.allowed_languages
        ):
            self.violations.add(
                linter.Violation(
                    rule_code=self.code,
                    rule_name=self.name,
                    rule_category=self.category,
                    line_number=self.line_number,
                    column_offset=self.column_offset,
                    line=self.line,
                    statement_location=self.statement_location,
                    description=f"Language '{node.plname}' is not allowed",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="If you want to allow this language, add the language to the"
                    " allowed languages list",
                ),
            )
