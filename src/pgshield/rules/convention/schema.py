"""Convention around schema."""

import abc
import typing

from pglast import ast, stream  # type: ignore[import-untyped]

from pgshield import utils, linter


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
        node: ast.Node,
    ) -> None:
        """Visit RangeVar. Checks relations during creation (do we want usage as well)."""  # noqa: E501
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_schema(
            node.schemaname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateEnumStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        enum_name = [
            stream.RawStream()(data_type).strip("'") for data_type in node.typeName
        ]

        schema_qualified = 2

        if len(enum_name) == schema_qualified:

            self._check_schema(
                enum_name[0],
                ancestors[statement_index].stmt_location,
                ancestors[statement_index],
            )

        else:

            self._check_schema(
                None,
                ancestors[statement_index].stmt_location,
                ancestors[statement_index],
            )

    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateFunctionStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        func_name = [
            stream.RawStream()(data_type).strip("'") for data_type in node.funcname
        ]

        schema_qualified = 2

        if len(func_name) == schema_qualified:

            self._check_schema(
                func_name[0],
                ancestors[statement_index].stmt_location,
                ancestors[statement_index],
            )

        else:

            self._check_schema(
                None,
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
        """Check that schema is in snake case."""
        if not schema and (location, self.code) not in self.ignore_rules:

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description="Object should be schema qualified",
                ),
            )


class SchemaWhitelisted(_Schema):
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
        print(schema)
        # print(self.config.get("lint.whitelist.schemas", []))
        # print(schema in self.config.get("lint.whitelist.schemas", []))
        schemas: str = self.config.get("lint.whitelist.schemas", [])
        print("pub" in schemas)
        print(type(schemas))
        print(schemas)
        if (
            schema
            and self.config.get("lint.whitelist.schemas")
            and schema not in self.config.get("lint.whitelist.schemas", [])
            and (location, self.code) not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description=f"Schema {schema} is not whitelisted",
                ),
            )
