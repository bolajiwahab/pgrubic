"""Unsafe storage operations."""

from pglast import ast, enums

from pgshield.core import linter


class DropTablespace(linter.Checker):
    """Drop tablespace."""

    name = "unsafe.drop_tablespace"
    code = "UNS001"

    def visit_DropTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropTableSpaceStmt,
    ) -> None:
        """Visit DropTableSpaceStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=ancestors[statement_index].stmt_location,
                column_offset=linter.get_column_offset(ancestors, node),
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
        node: ast.DropdbStmt,
    ) -> None:
        """Visit DropdbStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=ancestors[statement_index].stmt_location,
                column_offset=linter.get_column_offset(ancestors, node),
                statement=ancestors[statement_index],
                description="Drop database",
            ),
        )


class DropSchema(linter.Checker):
    """Drop schema."""

    name = "unsafe.drop_schema"
    code = "UNS003"

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.removeType == enums.ObjectType.OBJECT_SCHEMA:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Drop schema is not safe.",
                ),
            )
