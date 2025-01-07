"""Checker for extension whitelist."""

from pglast import ast, visitors

from pgrubic.core import linter


class ExtensionWhitelist(linter.BaseChecker):
    """## **What it does**
    Checks that an extension to be created is allowed.

    ## **Why not?**
    By default, any extension can be loaded into the database.
    This is quite dangerous as any bug causing a crash would mean a PostgreSQL would
    restart. So you not only want to empower **CREATE EXTENSION** to database owners,
    you also want to be able to review and explicitly allow extensions.

    ## **When should you?**
    Almost never. If an extension is not allowed, you are probably doing
    something wrong.

    ## **Use instead:**
    Extensions that are allowed.

    ## **Configuration**
    `allowed-extensions`: List of allowed extensions.
    """

    def visit_CreateExtensionStmt(
        self,
        ancestors: visitors.Ancestor,
        node: ast.CreateExtensionStmt,
    ) -> None:
        """Visit CreateExtensionStmt."""
        if (
            node.extname not in self.config.lint.allowed_extensions
            and "*" not in self.config.lint.allowed_extensions
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
                    description=f"Extension '{node.extname}' is not allowed",
                    is_auto_fixable=self.is_auto_fixable,
                    is_fix_enabled=self.is_fix_enabled,
                    help="If you want to allow this extension, add the extension to the"
                    " allowed extensions list",
                ),
            )
