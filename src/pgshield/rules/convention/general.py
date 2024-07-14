"""General convention."""

import re

from pglast import ast, enums, stream

from pgshield.core import linter


class PreferNonSQLASCIIEncoding(linter.Checker):
    """Prefer non sql_ascii encoding."""

    name: str = "convention.prefer_non_sql_ascii_encoding"
    code: str = "CVG001"

    is_auto_fixable: bool = False

    def visit_CreatedbStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreatedbStmt,
    ) -> None:
        """Visit CreatedbStmt."""
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

        if options.get("encoding") == "sql_ascii":

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer non sql_ascii encoding",
                ),
            )


class TableInheritance(linter.Checker):
    """## **What it does**
    Checks for usage of table inheritance.

    ## **Why not?**
    Table inheritance was a part of a fad wherein the database was closely coupled to
    object-oriented code. It turned out that coupling things that closely didn't
    actually produce the desired results.

    ## **When should you?**
    Never …almost. Now that table partitioning is done natively, that common use case
    for table inheritance has been replaced by a native feature that handles tuple
    routing, etc., without bespoke code. One of the very few exceptions would be
    temporal_tables extension if you are in a pinch and want to use that for row
    versioning in place of a lacking SQL 2011 support. Table inheritance will provide a
    small shortcut instead of using UNION ALL to get both historical as well as current
    rows. Even then you ought to be wary of caveats while working with parent table.

    ## **Use instead:**
    Don't use table inheritance. If you think you want to, use foreign keys instead.
    """

    name: str = "convention.usage_of_table_inheritance"
    code: str = "CVG002"

    is_auto_fixable: bool = False

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if node.inhRelations and not node.partbound:

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer declarative partitioning to table inheritance",
                ),
            )


class CreateRule(linter.Checker):
    """## **What it does**
    Checks for creation of rules.

    ## **Why not?**
    Rules are incredibly powerful, but they don't do what they look like they do.
    They look like they're some conditional logic, but they actually rewrite a query
    to modify it or add additional queries to it.

    ## **When should you?**
    Never. While the rewriter is an implementation detail of VIEWs,
    there is no reason to pry up this cover plate directly.

    ## **Use instead:**
    Don't use rules. If you think you want to, use a trigger instead.
    """

    name: str = "convention.prefer_trigger_over_rule"
    code: str = "CVG003"

    is_auto_fixable: bool = False

    def visit_RuleStmt(
        self,
        ancestors: ast.Node,
        node: ast.RuleStmt,
    ) -> None:
        """Visit RuleStmt."""
        self.violations.append(
            linter.Violation(
                statement_location=self.statement_location,
                statement_length=self.statement_length,
                node_location=self.node_location,
                description="Prefer trigger over rule",
            ),
        )


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


class TableShouldHavePrimaryKey(linter.Checker):
    """Table should have a primary key."""

    name: str = "convention.table_should_have_primary_key"
    code: str = "CVG007"

    is_auto_fixable: bool = False

    def _check_for_table_level_primary_key(
        self,
        node: ast.CreateStmt,
    ) -> bool:
        """Check for table level primary key."""
        return bool(
            (
                [
                    definition
                    for definition in node.tableElts
                    if isinstance(definition, ast.Constraint)
                    and definition.contype == enums.ConstrType.CONSTR_PRIMARY
                ]
            ),
        )

    def _check_for_column_level_primary_key(
        self,
        node: ast.CreateStmt,
    ) -> bool:
        """Check for column level primary key."""
        return bool(
            (
                [
                    definition
                    for definition in node.tableElts
                    if isinstance(definition, ast.ColumnDef) and definition.constraints
                    for constraint in definition.constraints
                    if constraint.contype == enums.ConstrType.CONSTR_PRIMARY
                ]
            ),
        )

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if (
            node.tableElts
            and not self._check_for_column_level_primary_key(node)
            and not self._check_for_table_level_primary_key(node)
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Table '{node.relation.relname}' should have a primary key",  # noqa: E501
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
