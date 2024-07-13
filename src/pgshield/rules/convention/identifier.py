"""Convention around identifiers."""

import abc

from pglast import ast, stream, keywords

from pgshield.core import linter


class _Identifier(abc.ABC, linter.Checker):
    """Base class for identifiers."""

    # To be overridden by subclasses
    name: str = ""
    code: str = ""
    is_auto_fixable: bool = False

    @abc.abstractmethod
    def _check_identifier(
        self,
        *,
        identifier: str | None,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check identifier."""
        ...

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        self._check_identifier(
            identifier=node.relation.relname,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors:

            self._check_identifier(
                identifier=node.colname,
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
            )

    def visit_ViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.ViewStmt,
    ) -> None:
        """Visit ViewStmt."""
        self._check_identifier(
            identifier=node.view.relname,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_CreateTableAsStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateTableAsStmt,
    ) -> None:
        """Visit CreateTableAsStmt."""
        self._check_identifier(
            identifier=node.into.rel.relname,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        self._check_identifier(
            identifier=node.idxname,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_CreateSeqStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateSeqStmt,
    ) -> None:
        """Visit CreateSeqStmt."""
        self._check_identifier(
            identifier=node.sequence.relname,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_CreateSchemaStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateSchemaStmt,
    ) -> None:
        """Visit CreateSchemaStmt."""
        self._check_identifier(
            identifier=node.schemaname,
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
        self._check_identifier(
            identifier=node.funcname[-1].sval,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_Constraint(
        self,
        ancestors: ast.Node,
        node: ast.Constraint,
    ) -> None:
        """Visit Constraint."""
        if node.conname is not None:
            self._check_identifier(
                identifier=node.conname,
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
            )

    def visit_CreatedbStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreatedbStmt,
    ) -> None:
        """Visit CreatedbStmt."""
        self._check_identifier(
            identifier=node.dbname,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_CreateRoleStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateRoleStmt,
    ) -> None:
        """Visit CreateRoleStmt."""
        self._check_identifier(
            identifier=node.role,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_CreateTableSpaceStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateTableSpaceStmt,
    ) -> None:
        """Visit CreateTableSpaceStmt."""
        self._check_identifier(
            identifier=node.tablespacename,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )

    def visit_CreateTrigStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateTrigStmt,
    ) -> None:
        """Visit CreateTrigStmt."""
        self._check_identifier(
            identifier=node.trigname,
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
        self._check_identifier(
            identifier=node.typeName[-1].sval,
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
        self._check_identifier(
            identifier=node.extname,
            statement_location=self.statement_location,
            statement_length=self.statement_length,
            node_location=self.node_location,
        )


class IsIdentifierInSnakeCase(_Identifier):
    """Identifier should be in snake case."""

    name: str = "convention.is_identifier_in_snake_case"
    code: str = "CVI001"
    is_auto_fixable: bool = False

    def _check_identifier(
        self,
        identifier: str | None,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check that identifier is in snake case."""
        if identifier and not stream.is_simple_name(identifier):

            self.violations.append(
                linter.Violation(
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description=f"Identifier '{identifier}' should be in snake case",
                ),
            )


class IsKeywordInIdentifier(_Identifier):
    """Is keyword in identifier."""

    name: str = "convention.is_keyword_in_identifier"
    code: str = "CVI002"

    def _check_identifier(
        self,
        identifier: str | None,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check for reserved keywords in identifier."""
        full_keywords: set[str] = (
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
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description=f"Identifier '{identifier}' should not use keyword",
                ),
            )


class IsSpecialCharacterInIdentifier(_Identifier):
    """Is special character in identifier."""

    name: str = "convention.is_special_character_in_identifier"
    code: str = "CVI004"

    def _check_identifier(
        self,
        identifier: str | None,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check that identifier does contain use special characters."""
        if identifier and not identifier.replace("_", "").isalnum():

            self.violations.append(
                linter.Violation(
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description=f"Identifier should not contain Special characters '{identifier}'",  # noqa: E501
                ),
            )


class IsPostgresPrefixInIdentifier(_Identifier):
    """Is pg_ in identifier."""

    name: str = "convention.is_pg_prefix_in_identifier"
    code: str = "CVI003"

    def _check_identifier(
        self,
        identifier: str | None,
        statement_location: int,
        statement_length: int,
        node_location: int,
    ) -> None:
        """Check that identifier does not start with pg_."""
        if identifier and identifier.startswith("pg_"):

            self.violations.append(
                linter.Violation(
                    statement_location=statement_location,
                    statement_length=statement_length,
                    node_location=node_location,
                    description="Identifier should not use prefix 'pg_'",
                ),
            )
