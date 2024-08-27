"""Convention for extensions."""

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
    """

    is_auto_fixable: bool = False

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
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Extension '{node.extname}' is not allowed",
                ),
            )
