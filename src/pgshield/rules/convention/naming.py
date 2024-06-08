"""Naming."""
from pglast import ast

from pgshield.core import linter


class IndexNaming(linter.Checker):  # type: ignore[misc]
    """Index naming."""

    name = "unsafe.index_naming"
    code = "CVN001"

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            not node.concurrent
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Non concurrent index creation",
                ),
            )
