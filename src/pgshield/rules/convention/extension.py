"""Convention for extensions."""

from pglast import ast

from pgshield.core import linter


class IsExtensionWhitelisted(linter.Checker):
    """Is extension whitelisted."""

    name: str = "convention.is_extension_whitelisted"
    code: str = "CVE001"

    is_auto_fixable: bool = False

    def visit_CreateExtensionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateExtensionStmt,
    ) -> None:
        """Visit CreateExtensionStmt."""
        if node.extname not in self.config.extensions:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Extension '{node.extname}' is not whitelisted",
                ),
            )
