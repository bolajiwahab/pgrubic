"""Rules for schema."""

import abc

from pglast import ast

from pgshield.core import linter


class Schema(abc.ABC, linter.Checker):
    """Schema details for relations, enums, functions, sequences, views."""

    # To be overridden by subclasses
    is_auto_fixable: bool = False

    @abc.abstractmethod
    def _check_schema(
        self,
        *,
        schema_name: str | None,
        statement_length: int,
        statement_location: int,
        node_location: int,
    ) -> None:
        """Check schema."""
        ...

    def visit_RangeVar(
        self,
        ancestors: ast.Node,
        node: ast.RangeVar,
    ) -> None:
        """Visit RangeVar."""
        # skip DMLs
        if not isinstance(
            abs(ancestors).node,
            ast.SelectStmt | ast.InsertStmt | ast.UpdateStmt | ast.DeleteStmt,
        ):

            self._check_schema(
                schema_name=node.schemaname,
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
            )

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        schema_name: str = node.typeName[0].sval if len(node.typeName) > 1 else None

        self._check_schema(
            schema_name=schema_name,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        schema_name: str = node.funcname[0].sval if len(node.funcname) > 1 else None

        self._check_schema(
            schema_name=schema_name,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )
