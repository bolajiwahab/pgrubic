"""Unsafe storage operations."""

from pglast import ast, enums

from pgshield.core import linter


class DropTablespace(linter.Checker):
    """Drop tablespace."""

    name: str = "unsafe.drop_tablespace"
    code: str = "UNS001"

    is_auto_fixable: bool = False

    def visit_DropTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropTableSpaceStmt,
    ) -> None:
        """Visit DropTableSpaceStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Drop tablespace",
            ),
        )


class DropDatabase(linter.Checker):
    """Drop database."""

    name: str = "unsafe.drop_database"
    code: str = "UNS002"

    is_auto_fixable: bool = False

    def visit_DropdbStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropdbStmt,
    ) -> None:
        """Visit DropdbStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Drop database",
            ),
        )


class DropSchema(linter.Checker):
    """Drop schema."""

    name: str = "unsafe.drop_schema"
    code: str = "UNS003"

    is_auto_fixable: bool = False

    def visit_DropStmt(
        self,
        ancestors: ast.Node,
        node: ast.DropStmt,
    ) -> None:
        """Visit DropStmt."""
        if node.removeType == enums.ObjectType.OBJECT_SCHEMA:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Drop schema is not safe",
                ),
            )
