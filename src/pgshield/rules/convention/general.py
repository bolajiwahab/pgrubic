"""General convention."""

import re

from pglast import ast, stream

from pgshield.core import linter


class PreferNonSQLASCIIEncoding(linter.Checker):
    """Prefer non sql_ascii encoding."""

    name: str = "convention.prefer_non_sql_ascii_encoding"
    code: str = "CVG001"

    fixable: bool = False

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

    fixable: bool = False

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

    fixable: bool = False

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

    fixable: bool = True

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        required_columns: list[str] = list(self.config.required_columns.keys())

        if node.tableElts:

            statement_index: int = linter.get_statement_index(ancestors)

            given_columns: list[str] = [
                column.colname
                for column in node.tableElts
                if isinstance(column, ast.ColumnDef)
            ]

            for column in required_columns:

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
                                        {"@": "String", "sval": "timestamp"}, # need to fetch from dictionary
                                    ),
                                ),
                            ),
                        )


class PreferLookUpTableOverEnum(linter.Checker):
    """Prefer look up table over enum."""

    name = "convention.prefer_look_up_table_over_enum"
    code = "CVG005"

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
