"""General convention."""

import re

from pglast import ast, stream

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
        statement_index: int = linter.get_statement_index(ancestors)

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
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer non sql_ascii encoding",
                ),
            )


class PreferDeclarativePartitioningToTableInheritance(linter.Checker):
    """Prefer declarative partitioning to table inheritance."""

    name: str = "convention.prefer_declarative_partitioning_to_table_inheritance"
    code: str = "CVG002"

    is_auto_fixable: bool = False

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        if node.inhRelations and not node.partbound:

            statement_index: int = linter.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer declarative partitioning to table inheritance",
                ),
            )


class PreferTriggerOverRule(linter.Checker):
    """Prefer trigger over rule."""

    name: str = "convention.prefer_trigger_over_rule"
    code: str = "CVG003"

    is_auto_fixable: bool = False

    def visit_RuleStmt(
        self,
        ancestors: ast.Node,
        node: ast.RuleStmt,
    ) -> None:
        """Visit RuleStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=ancestors[statement_index].stmt_location,
                column_offset=linter.get_column_offset(ancestors, node),
                statement=ancestors[statement_index],
                description="Prefer trigger over rule",
            ),
        )


class MissingRequiredColumn(linter.Checker):
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

            statement_index: int = linter.get_statement_index(ancestors)

            given_columns: list[str] = [
                column.colname
                for column in node.tableElts
                if isinstance(column, ast.ColumnDef)
            ]

            for column, data_type in self.config.required_columns.items():

                if column not in given_columns:

                    self.violations.append(
                        linter.Violation(
                            lineno=ancestors[statement_index].stmt_location,
                            column_offset=linter.get_column_offset(ancestors, node),
                            statement=ancestors[statement_index],
                            description=f"Column '{column}' is required",
                        ),
                    )

                    if self.config.fix is True:

                        node.tableElts = (
                            *node.tableElts,
                            ast.ColumnDef(
                                colname=column,
                                typeName=ast.TypeName(
                                    names=(
                                        {
                                            "@": "String",
                                            "sval": data_type,
                                        },
                                    ),
                                ),
                            ),
                        )


class PreferLookUpTableOverEnum(linter.Checker):
    """Prefer look up table over enum."""

    name = "convention.prefer_look_up_table_over_enum"
    code = "CVG005"

    is_auto_fixable: bool = False

    def visit_CreateEnumStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateEnumStmt,
    ) -> None:
        """Visit CreateEnumStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                lineno=ancestors[statement_index].stmt_location,
                column_offset=linter.get_column_offset(ancestors, node),
                statement=ancestors[statement_index],
                description="Prefer look up table over enum",
            ),
        )


class PreferIndexElementsUpToThree(linter.Checker):
    """Prefer index elements up to three."""

    name = "convention.prefer_index_elements_up_to_three"
    code = "CVG006"

    is_auto_fixable: bool = False

    def visit_IndexStmt(
        self,
        ancestors: ast.Node,
        node: ast.IndexStmt,
    ) -> None:
        """Visit IndexStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        max_index_elements = 3

        if len(node.indexParams) > max_index_elements:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer index elements up to three",
                ),
            )


class PreferPartitioningByOneKey(linter.Checker):
    """Prefer partitioning by one key."""

    name = "convention.prefer_partitioning_by_one_key"
    code = "CVG007"

    is_auto_fixable: bool = False

    def visit_PartitionSpec(
        self,
        ancestors: ast.Node,
        node: ast.PartitionSpec,
    ) -> None:
        """Visit PartitionSpec."""
        statement_index: int = linter.get_statement_index(ancestors)

        max_partition_elements = 1

        if len(node.partParams) > max_partition_elements:

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer partitioning by one key",
                ),
            )
