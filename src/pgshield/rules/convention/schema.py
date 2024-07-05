"""Convention around schema."""

import re
import abc

from pglast import ast, stream

from pgshield.core import linter


class _Schema(abc.ABC, linter.Checker):
    """Schema details for table, types, functions, sequences, views."""

    # To be overridden by subclasses
    name: str = ""
    code: str = ""
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
        create = [
            ast.CreateStmt,
            ast.CreateTableAsStmt,
            ast.CreateSeqStmt,
            ast.ViewStmt,
        ]

        for stmt in create:

            if stmt in ancestors:

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
        schema_name = node.typeName[0].sval if len(node.typeName) != 1 else None

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
        schema_name = node.funcname[0].sval if len(node.funcname) != 1 else None

        self._check_schema(
            schema_name=schema_name,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_CreateExtensionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateExtensionStmt,
    ) -> None:
        """Visit CreateExtensionStmt."""
        options: dict[str, str] = (
            {
                re.sub(r"\s*", "", stream.RawStream()(option), flags=re.UNICODE)
                .split("=")[0]: re.sub(
                    r"\s*",
                    "",
                    stream.RawStream()(option),
                    flags=re.UNICODE,
                )
                .split("=")[1]
                .strip("'")
                for option in node.options
            }
            if node.options is not None
            else {}
        )

        self._check_schema(
            schema_name=options.get("schema"),
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )


class SchemaQualified(_Schema):
    """Schema details for table, types, functions, sequences, views."""

    name = "convention.schema_qualified"
    code = "CVS001"

    is_auto_fixable: bool = False

    def _check_schema(
        self,
        schema_name: str | None,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check that object is schema qualified."""
        if not schema_name:

            self.violations.append(
                linter.Violation(
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description="Database object should be schema qualified",
                ),
            )


class SchemasWhitelisted(_Schema):
    """Only whitelisted schemas are allowed."""

    name = "convention.whitelisted_schemas"
    code = "CVS002"

    is_auto_fixable: bool = False

    def _check_schema(
        self,
        schema_name: str | None,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check schema is whitelisted."""
        if (
            schema_name
            and self.config.schemas
            and schema_name not in self.config.schemas
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description=f"Schema '{schema_name}' is not whitelisted",
                ),
            )
