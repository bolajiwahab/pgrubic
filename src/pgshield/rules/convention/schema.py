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
        # View has been intentionally excluded here as recursive cte in recursive view
        # is not schema qualified.
        # https://www.postgresql.org/docs/16/sql-createview.html#:~:text=Notice%20that%20although%20the%20recursive%20view%27s%20name%20is%20schema%2Dqualified%20in%20this%20CREATE%2C%20its%20internal%20self%2Dreference%20is%20not%20schema%2Dqualified.%20This%20is%20because%20the%20implicitly%2Dcreated%20CTE%27s%20name%20cannot%20be%20schema%2Dqualified.
        if ast.ViewStmt not in ancestors:

            self._check_schema(
                schema_name=node.schemaname,
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
        # We are only checking that the view is schema qualified here.
        # We do not check the body of the query as it can be of any forms.
        self._check_schema(
            schema_name=node.view.schemaname,
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
        schema_name: str =  node.typeName[0].sval if len(node.typeName) != 1 else None

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
        schema_name: str =  node.funcname[0].sval if len(node.funcname) != 1 else None

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


class DatabaseObjectShouldSchemaQualified(_Schema):
    """Database object should be schema qualified."""

    name: str =  "convention.database_object_should_schema_qualified"
    code: str = "CVS001"

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

    name: str =  "convention.whitelisted_schemas"
    code: str = "CVS002"

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
