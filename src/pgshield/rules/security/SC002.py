"""Convention for extensions."""

from pglast import ast

from pgshield.core import linter


class ProceduralLanguageWhitelist(linter.Checker):
    """## **What it does**
    Checks that a procedural language to be created is whitelisted.

    ## **Why not?**
    By default, any procedural language can be loaded into the database.
    This is quite dangerous as some unsafe operations might be introuduced by languages.
    So you not only want to empower **CREATE LANGUAGE** to database owners, you
    also want to be able to review and explicitly whitelist the allowed languages.

    ## **When should you?**
    Almost never. If a procedural language is not allowed, you are probably doing
    something wrong.

    ## **Use instead:**
    Procedural languages that are in the whitelist.
    """

    name: str = "security.procedureal_language_whitelist"
    code: str = "SC002"

    is_auto_fixable: bool = False

    def visit_CreatePLangStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreatePLangStmt,
    ) -> None:
        """Visit CreatePLangStmt."""
        if (
            node.plname not in self.config.languages
            and "*" not in self.config.languages
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Language '{node.plname}' is not whitelisted",
                ),
            )
