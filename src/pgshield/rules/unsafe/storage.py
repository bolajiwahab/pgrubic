"""Unsafe storage operations."""

from pglast import ast  # type: ignore[import-untyped]

from pgshield import utils, linter


class DropTablespace(linter.Checker):
    """Drop tablespace."""

    name = "unsafe.drop_tablespace"
    code = "UNS001"

    def visit_DropTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,  # noqa: ARG002
    ) -> None:
        """Visit DropTableSpaceStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ancestors[statement_index].stmt_location,
            self.code,
        ) not in self.ignore_rules:

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Drop tablespace",
                ),
            )


class DropDatabase(linter.Checker):
    """Drop database."""

    name = "unsafe.drop_database"
    code = "UNS002"

    def visit_DropdbStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,  # noqa: ARG002
    ) -> None:
        """Visit DropdbStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            ancestors[statement_index].stmt_location,
            self.code,
        ) not in self.ignore_rules:
            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Drop database",
                ),
            )
