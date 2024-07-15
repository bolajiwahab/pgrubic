"""General convention."""

import re

from pglast import ast, enums, stream

from pgshield.core import linter


class RequiredColumn(linter.Checker):
    """Missing required column."""

    name: str = "convention.missing_required_column"
    code: str = "CVG004"

    is_auto_fixable: bool = True

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if node.tableElts:

            given_columns: list[str] = [
                column.colname
                for column in node.tableElts
                if isinstance(column, ast.ColumnDef)
            ]

            for column in self.config.required_columns:

                if column.name not in given_columns:

                    self.violations.append(
                        linter.Violation(
                            statement_location=self.statement_location,
                            statement_length=self.statement_length,
                            node_location=self.node_location,
                            description=f"Column '{column.name}' of type"
                            f" '{column.data_type}' is required",
                        ),
                    )

                    if self.config.fix is True:

                        node.tableElts = (
                            *node.tableElts,
                            ast.ColumnDef(
                                colname=column.name,
                                typeName=ast.TypeName(
                                    names=(
                                        {
                                            "@": "String",
                                            "sval": column.data_type,
                                        },
                                    ),
                                ),
                            ),
                        )


class PreferLookUpTableOverEnum(linter.Checker):
    """Prefer look up table over enum."""

    name: str = "convention.prefer_look_up_table_over_enum"
    code: str = "CVG005"

    is_auto_fixable: bool = False

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Prefer look up table over enum",
            ),
        )


class PreferIndexElementsUpToThree(linter.Checker):
    """Prefer index elements up to three."""

    name: str = "convention.prefer_index_elements_up_to_three"
    code: str = "CVG006"

    is_auto_fixable: bool = False

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        max_index_elements = 3

        if len(node.indexParams) > max_index_elements:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Prefer index elements up to {max_index_elements}",
                ),
            )


class BooleanFieldShouldBeNonNullable(linter.Checker):
    """Boolean field should be non-nullable."""

    name: str = "convention.boolean_field_should_be_non_nullable"
    code: str = "CVG008"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors
        ) and node.typeName.names[-1].sval == "bool":

            is_not_null = bool(
                (
                    [
                        constraint
                        for constraint in node.constraints
                        if constraint.contype == enums.ConstrType.CONSTR_NOTNULL
                    ]
                    if node.constraints is not None
                    else []
                ),
            )

            if not is_not_null:

                self.violations.append(
                    linter.Violation(
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                        description="Boolean field should be non-nullable",
                    ),
                )


class PreferReplaceForFunction(linter.Checker):
    """Prefer replace for function."""

    name: str = "convention.prefer_replace_for_function"
    code: str = "CVG009"

    is_auto_fixable: bool = False

    def visit_CreateFunctionStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateFunctionStmt,
    ) -> None:
        """Visit CreateFunctionStmt."""
        if not node.replace:
            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer replace for function",
                ),
            )


class PreferReplaceForView(linter.Checker):
    """Prefer replace for view."""

    name: str = "convention.prefer_replace_for_view"
    code: str = "CVG010"

    is_auto_fixable: bool = False

    def visit_ViewStmt(
        self,
        ancestors: ast.Node,
        node: ast.ViewStmt,
    ) -> None:
        """Visit ViewStmt."""
        if not node.replace:
            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer replace for view",
                ),
            )


class ForbidRedefinitionOfTableColumn(linter.Checker):
    """Forbid redefinition of table column."""

    name: str = "convention.forbid_redefinition_of_table_column"
    code: str = "CVG011"

    is_auto_fixable: bool = True

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if node.tableElts:

            given_columns: list[str] = [
                column.colname
                for column in node.tableElts
                if isinstance(column, ast.ColumnDef)
            ]

            duplicates: set[str] = {
                x for x in given_columns if given_columns.count(x) > 1
            }

            for column in duplicates:

                self.violations.append(
                    linter.Violation(
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                        description=f"Column '{column}' specified more than once",
                    ),
                )

            if node.relation.relname in given_columns:

                self.violations.append(
                    linter.Violation(
                        statement_location=self.statement_location,
                        statement_length=self.statement_length,
                        node_location=self.node_location,
                        description=f"Table '{node.relation.relname}' found in columns",
                    ),
                )
