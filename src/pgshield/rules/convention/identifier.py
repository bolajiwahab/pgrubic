"""Convention around identifiers."""

import typing

import inflection
from pglast import ast, stream, keywords  # type: ignore[import-untyped]

from pgshield import utils, linter


class Identifier(linter.Checker):  # type: ignore[misc]
    """Various checks around identifier."""

    name = ""
    code = "COV021"

    def _check_identifier(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Check identifier."""
        functions: list[typing.Callable] = [
            self._check_identifier_for_upper_case,
            self._check_identifier_for_reserved_keywords,
            self._check_identifier_for_special_characters,
            self._check_identifier_is_in_snake_case,
        ]

        for method in functions:
            method(*args, **kwargs)

    def _check_identifier_for_upper_case(
        self,
        identifier: str,
        location: int,
        statement: str,
    ) -> None:
        """Check for uppercase in identifier."""
        self.name = "convention.uppercase_in_identifier"

        if any(ele.isupper() for ele in identifier):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description=f"Uppercase found in '{identifier}' identifier",
                ),
            )

    def _check_identifier_is_in_snake_case(
        self,
        identifier: str,
        location: int,
        statement: str,
    ) -> None:
        """Check identifier is snake case."""
        self.name = "convention.check_identifier_is_snake_case"

        if identifier != inflection.underscore(identifier):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description=f"Identifier '{identifier}' is not in snake case",
                ),
            )

    def _check_identifier_for_reserved_keywords(
        self,
        identifier: str,
        location: int,
        statement: str,
    ) -> None:
        """Check for reserved keywords in identifiers."""
        self.name = "convention.reserved_keywords_in_identifier"

        full_keywords = (
            set(keywords.RESERVED_KEYWORDS)
            .union(
                set(keywords.UNRESERVED_KEYWORDS),
            )
            .union(keywords.COL_NAME_KEYWORDS)
            .union(keywords.TYPE_FUNC_NAME_KEYWORDS)
        )

        if identifier in (full_keywords):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description=f"Reserved keyword '{identifier}' found in identifier",
                ),
            )

    def _check_identifier_for_special_characters(
        self,
        identifier: str,
        location: int,
        statement: str,
    ) -> None:
        """Check for special characters in identifier."""
        self.name = "convention.special_characters_in_identifier"

        if not identifier.replace("_", "").isalnum():

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description=f"Special characters found in '{identifier}' identifier",  # noqa: E501
                ),
            )

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier(
            node.relation.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        if ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors:

            statement_index: int = utils.get_statement_index(ancestors)

            self._check_identifier_for_upper_case(
                node.colname,
                ancestors[statement_index].stmt_location,
                ancestors[statement_index],
            )

    def visit_ViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ViewStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier_for_upper_case(
            node.view.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateTableAsStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateTableAsStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier_for_upper_case(
            node.into.rel.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit IndexStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier_for_upper_case(
            node.idxname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateSeqStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateSeqStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier_for_upper_case(
            node.sequence.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateSchemaStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateSchemaStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier_for_upper_case(
            node.schemaname,
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

        self._check_identifier_for_upper_case(
            func_name[-1],
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = utils.get_statement_index(ancestors)

        if node.conname is not None:
            self._check_identifier_for_upper_case(
                node.conname,
                ancestors[statement_index].stmt_location,
                ancestors[statement_index],
            )

    def visit_CreatedbStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreatedbStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier_for_upper_case(
            node.dbname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateRoleStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateRoleStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier_for_upper_case(
            node.role,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateTableSpaceStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier_for_upper_case(
            node.tablespacename,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateTrigStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateTrigStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        self._check_identifier_for_upper_case(
            node.trigname,
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

        type_name = [
            stream.RawStream()(data_type).strip("'") for data_type in node.typeName
        ]

        self._check_identifier_for_upper_case(
            type_name[-1],
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )
