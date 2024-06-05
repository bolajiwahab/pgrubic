from typing import ClassVar

from pglast import ast, enums, stream, keywords  # type: ignore[import-untyped]

from pgshield import utils, linter

class Identifiers(linter.Checker):  # type: ignore[misc]
    """No upper case name for identifiers."""

    name = "convention.no_upper_case_name_for_identifiers"
    code = "CVN011"

    identifiers: ClassVar[list[tuple[int, str]]] = []

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self.identifiers.append((statement_index, node.relation.relname))
