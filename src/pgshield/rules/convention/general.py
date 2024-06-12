"""General convention."""

import re

from pglast import ast, stream  # type: ignore[import-untyped]

from pgshield.core import linter


class PreferNonSQLASCIIEncoding(linter.Checker):
    """Prefer non sql_ascii encoding."""

    name = "convention.prefer_non_sql_ascii_encoding"
    code = "CVG001"

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
                .split("=")[0]
                .lower(): re.sub(
                    r"\s*",
                    "",
                    stream.RawStream()(option),
                    flags=re.UNICODE,
                )
                .split("=")[1]
                .strip("'")
                .lower()
                for option in node.options
            }
            if node.options is not None
            else {}
        )

        if options.get("encoding") == "sql_ascii":

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer non sql_ascii encoding",
                ),
            )


class PreferDeclarativePartitioningToTableInheritance(linter.Checker):
    """Prefer declarative partitioning to table inheritance."""

    name = "convention.prefer_declarative_partitioning_to_table_inheritance"
    code = "CVG002"

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.inhRelations and not node.partbound:

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer declarative partitioning to table inheritance",
                ),
            )


class PreferTriggerOverRule(linter.Checker):
    """Prefer trigger over rule."""

    name = "convention.prefer_trigger_over_rule"
    code = "CVG003"

    def visit_RuleStmt(
        self,
        ancestors: ast.Node,
        node: ast.RuleStmt,  # noqa: ARG002
    ) -> None:
        """Visit RuleStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        self.violations.append(
            linter.Violation(
                location=ancestors[statement_index].stmt_location,
                statement=ancestors[statement_index],
                description="Prefer trigger over rule",
            ),
        )


class MissingRequiredColumn(linter.Checker):
    """Missing required column."""

    name = "convention.missing_required_column"
    code = "CVG004"

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if node.tableElts:
            # print(stream.RawStream()(node.tableElts))

            for column in list(self.config.required_columns.keys()):

                for col in node.tableElts:
                    print(col.colname)

                if column not in node.tableElts:

                    self.violations.append(
                        linter.Violation(
                            location=ancestors[statement_index].stmt_location,
                            statement=ancestors[statement_index],
                            description=f"{list(self.config.required_columns.keys())} columns are required.",  # noqa: E501
                        ),
                    )
