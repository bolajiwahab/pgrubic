"""Unsafe storage operations."""

from pglast import ast, enums

from pgshield.core import linter


class DropTablespace(linter.Checker):
    """Drop tablespace."""

    name = "unsafe.drop_tablespace"
    code = "UNS001"

    is_auto_fixable: bool = False

    def visit_DropTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropTableSpaceStmt,
    ) -> None:
        """Visit DropTableSpaceStmt."""
        statement: linter.Statement = linter.get_statement_details(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=statement.location,
                column_offset=linter.get_node_location(node),
                statement=ancestors[statement],
                description="Drop tablespace",
            ),
        )


class DropDatabase(linter.Checker):
    """Drop database."""

    name = "unsafe.drop_database"
    code = "UNS002"

    is_auto_fixable: bool = False

    def visit_DropdbStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropdbStmt,
    ) -> None:
        """Visit DropdbStmt."""
        statement: linter.Statement = linter.get_statement_details(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=statement.location,
                column_offset=linter.get_node_location(node),
                statement=ancestors[statement],
                description="Drop database",
            ),
        )


class DropSchema(linter.Checker):
    """Drop schema."""

    name = "unsafe.drop_schema"
    code = "UNS003"

    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        statement: linter.Statement = linter.get_statement_details(ancestors)

        if node.removeType == enums.ObjectType.OBJECT_SCHEMA:

            self.violations.append(
                linter.Violation(
                    lineno=statement.location,
                    column_offset=linter.get_node_location(node),
                    statement=ancestors[statement],
                    description="Drop schema is not safe.",
                ),
            )
