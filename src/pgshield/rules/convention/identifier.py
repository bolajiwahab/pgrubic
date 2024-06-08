"""Convention around identifiers."""

import abc
import typing

import inflection
from pglast import ast, keywords  # type: ignore[import-untyped]

from pgshield.core import linter


class _Identifier(abc.ABC, linter.Checker):  # type: ignore[misc]
    """Get identifiers."""

    # To be overridden by subclasses
    name = ""
    code = ""

    @abc.abstractmethod
    def _check_identifier(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        """Check identifier."""
        ...

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.relation.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors:

            statement_index: int = linter.get_statement_index(ancestors)

            self._check_identifier(
                node.colname,
                ancestors[statement_index].stmt_location,
                ancestors[statement_index],
            )

    def visit_ViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.ViewStmt,
    ) -> None:
        """Visit ViewStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.view.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateTableAsStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateTableAsStmt,
    ) -> None:
        """Visit CreateTableAsStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.into.rel.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.idxname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateSeqStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateSeqStmt,
    ) -> None:
        """Visit CreateSeqStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.sequence.relname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateSchemaStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateSchemaStmt,
    ) -> None:
        """Visit CreateSchemaStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.schemaname,
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

        self._check_identifier(
            node.funcname[-1].sval,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.conname is not None:
            self._check_identifier(
                node.conname,
                ancestors[statement_index].stmt_location,
                ancestors[statement_index],
            )

    def visit_CreatedbStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreatedbStmt,
    ) -> None:
        """Visit CreatedbStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.dbname,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateRoleStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateRoleStmt,
    ) -> None:
        """Visit CreateRoleStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.role,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateTableSpaceStmt,
    ) -> None:
        """Visit CreateTableSpaceStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.tablespacename,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )

    def visit_CreateTrigStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateTrigStmt,
    ) -> None:
        """Visit CreateTrigStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self._check_identifier(
            node.trigname,
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

        self._check_identifier(
            node.typeName[-1].sval,
            ancestors[statement_index].stmt_location,
            ancestors[statement_index],
        )


class SnakeCase(_Identifier):  # type: ignore[misc]
    """Identifier should be in snake case."""

    name = "convention.snake_case_identifier"
    code = "CVI001"

    def _check_identifier(
        self,
        identifier: str,
        location: int,
        statement: str,
    ) -> None:
        """Check that identifier is in snake case."""
        if (
            identifier != inflection.underscore(identifier)
            and (location, self.code) not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description=f"Identifier '{identifier}' should be in snake case",
                ),
            )


class Keywords(_Identifier):  # type: ignore[misc]
    """Identifier should not contain reserved keywords."""

    name = "convention.reserved_keywords_in_identifier"
    code = "CVI002"

    def _check_identifier(
        self,
        identifier: str,
        location: int,
        statement: str,
    ) -> None:
        """Check for reserved keywords in identifier."""
        full_keywords = (
            set(keywords.RESERVED_KEYWORDS)
            .union(
                set(keywords.UNRESERVED_KEYWORDS),
            )
            .union(keywords.COL_NAME_KEYWORDS)
            .union(keywords.TYPE_FUNC_NAME_KEYWORDS)
        )

        if (
            identifier in (full_keywords)
            and (location, self.code) not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description=f"Identifier should not use keywords '{identifier}'",
                ),
            )


class SpecialCharacters(_Identifier):  # type: ignore[misc]
    """Identifier should not contain special characters."""

    name = "convention.special_characters_in_identifier"
    code = "CVI004"

    def _check_identifier(
        self,
        identifier: str,
        location: int,
        statement: str,
    ) -> None:
        """Check that identifier is in snake case."""
        if (
            not identifier.replace("_", "").isalnum()
            and (location, self.code) not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description=f"Identifier should not use Special characters '{identifier}'",  # noqa: E501
                ),
            )


class PostgresPrefix(_Identifier):  # type: ignore[misc]
    """Identifier should not start with pg_ ."""

    name = "convention.pg_prefix_in_identifier"
    code = "CVI003"

    def _check_identifier(
        self,
        identifier: str,
        location: int,
        statement: str,
    ) -> None:
        """Check that identifier does not start with pg_."""
        if (
            identifier.startswith("pg_")
            and (location, self.code) not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=location,
                    statement=statement,
                    description="Identifier should not use prefix 'pg_'",
                ),
            )
