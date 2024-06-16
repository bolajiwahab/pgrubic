"""Whitelisted extensions."""

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
        statement_index: int = linter.get_statement_index(ancestors)

        if node.extname not in self.config.extensions:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description=f"Extension '{node.extname}' is not whitelisted",
                ),
            )
