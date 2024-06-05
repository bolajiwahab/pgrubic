"""Convention around schema qualified."""

import typing

from pglast import ast, stream, keywords  # type: ignore[import-untyped]

from pgshield import utils, linter


class ObjectShouldBeSchemaQualified(linter.Checker):  # type: ignore[misc]
    """Objects should be schema-qualified. E.g table, types, functions, sequences, views."""  # noqa: E501

    name = "convention.database_object_should_be_schema_qualified"
    code = "COV022"


    def visit_RangeVar(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit RangeVar. Checks relations during creation and usage."""
        statement_index: int = utils.get_statement_index(ancestors)

        if not node.schemaname:
            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Relation should be schema-qualified",
                ),
            )

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateEnumStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        type_name = [
            stream.RawStream()(data_type).strip("'") for data_type in node.typeName
        ]

        schema_qualified = 2

        if len(type_name) != schema_qualified:

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Type should be schema-qualified",
                ),
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

        if len(func_name) != schema_qualified:

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Function should be schema-qualified",
                ),
            )
