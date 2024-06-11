"""Convention around schema."""

import re
import abc
import typing

from pglast import ast, stream  # type: ignore[import-untyped]

from pgshield.core import linter


class _Schema(abc.ABC, linter.Checker):  # type: ignore[misc]
    """Schema details for table, types, functions, sequences, views."""

    # To be overridden by subclasses
    name = ""
    code = ""

    @abc.abstractmethod
    def _check_schema(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Check schema."""
        ...

    def visit_RangeVar(
        self,
        ancestors: ast.Node,
        node: ast.RangeVar,
    ) -> None:
        """Visit RangeVar."""
        statement_index: int = linter.get_statement_index(ancestors)

        create = [
            ast.CreateStmt,
            ast.CreateTableAsStmt,
            ast.CreateSeqStmt,
            ast.ViewStmt,
        ]

        for stmt in create:

            if stmt in ancestors:

                self._check_schema(
                    node.schemaname,
                    ancestors[statement_index].stmt_location,
                    ancestors[statement_index],
                )

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        schema_name = node.typeName[0].sval if len(node.typeName) != 1 else None

        self._check_schema(
            schema_name,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )


    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        schema_name = node.funcname[0].sval if len(node.funcname) != 1 else None

        self._check_schema(
            schema_name,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateExtensionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateExtensionStmt,
    ) -> None:
        """Visit CreateExtensionStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        options: dict[str, str] = (
            {
                re.sub(r"\s*", "", stream.RawStream()(option), flags=re.UNICODE)
                .split("=")[0]
                .lower(): re.sub(
                    r"\s*",
                    "",
                    stream.RawStream()(option),
                    flags=re.UNICODE,
                )
                .split("=")[1]
                .strip("'")
                .lower()
                for option in node.options
            }
            if node.options is not None
            else {}
        )

        self._check_schema(
            options.get("schema"),
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )


class SchemaQualified(_Schema):
    """Schema details for table, types, functions, sequences, views."""

    name = "convention.schema_qualified"
    code = "CVS001"

    def _check_schema(
        self,
        schema: str | None,
        location: int,
        statement: str,
    ) -> None:
        """Check that object is schema qualified."""
        if not schema and (location, self.code) not in self.ignore_rules:

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description="Object should be schema qualified",
                ),
            )


class SchemasWhitelisted(_Schema):
    """Only whitelisted schemas are allowed."""

    name = "convention.whitelisted_schemas"
    code = "CVS002"

    def _check_schema(
        self,
        schema: str | None,
        location: int,
        statement: str,
    ) -> None:
        """Check schema is whitelisted."""
        if (
            schema
            and self.config.schemas and schema not in self.config.schemas
            and (location, self.code) not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description=f"Schema '{schema}' is not whitelisted",
                ),
            )
