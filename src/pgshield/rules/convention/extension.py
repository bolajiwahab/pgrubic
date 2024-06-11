"""Whitelisted extensions."""
from pglast import ast  # type: ignore[import-untyped]

from pgshield.core import linter


class ExtensionWhitelisted(linter.Checker):
    """Only whitelisted extensions are allowed."""

    name = "convention.whitelisted_extension"
    code = "CVE001"

    def visit_CreateExtensionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateExtensionStmt,
    ) -> None:
        """Visit CreateExtensionStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.extname not in self.config.extensions:

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description=f"Extension '{node.extname}' is not whitelisted",
                ),
            )
