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


class PreferTimestampWithTimezoneOverTimestampWithoutTimezone(linter.Checker):
    """Prefer timestamp with timezone over timestamp without timezone."""

    name = "convention.prefer_timestamp_with_timezone_over_timestamp_without_timezone"
    code = "CVG006"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "timestamp"
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer timestamp with timezone over timestamp without timezone",  # noqa: E501
                ),
            )


class PreferTimestampWithTimezoneOverTimeWithTimezone(linter.Checker):
    """Prefer timestamp with timezone over time with timezone."""

    name = "convention.prefer_timestamp_with_timezone_over_time_with_timezone"
    code = "CVG007"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (node.typeName.names[-1].sval == "timetz"):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer timestamp with timezone over time with timezone",  # noqa: E501
                ),
            )


class PreferEntireTimestampWithoutTimezone(linter.Checker):
    """Prefer entire timestamp without timezone."""

    name = "convention.prefer_entire_timestamp_without_timezone"
    code = "CVG008"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "timestamp" and node.typeName.typmods
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer entire timestamp without timezone",
                ),
            )


class PreferEntireTimestampWithTimezone(linter.Checker):
    """Prefer entire timestamp with timezone."""

    name = "convention.prefer_entire_timestamp_with_timezone"
    code = "CVG009"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "timestamptz" and node.typeName.typmods
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer entire timestamp with timezone",
                ),
            )


class PreferTextOverChar(linter.Checker):
    """Prefer text over char."""

    name = "convention.prefer_text_over_char"
    code = "CVG010"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval in ["bpchar", "char"]
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer text over char",
                ),
            )


class PreferTextOverVarChar(linter.Checker):
    """Prefer text over varchar."""

    name = "convention.prefer_text_over_var_char"
    code = "CVG011"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (node.typeName.names[-1].sval == "varchar"):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer text over varchar",
                ),
            )


class PreferNumericOverMoney(linter.Checker):
    """Prefer numeric over money."""

    name = "convention.prefer_numeric_over_money"
    code = "CVG012"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (node.typeName.names[-1].sval == "money"):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer numeric over money",
                ),
            )


class PreferIdentityColumnOverSerial(linter.Checker):
    """Prefer identity column over serial."""

    name = "convention.prefer_identity_column_over_serial"
    code = "CVG013"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (node.typeName.names[-1].sval == "serial"):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer identity column over serial",
                ),
            )


class PreferIdentityColumnOverBigSerial(linter.Checker):
    """Prefer identity column over bigserial."""

    name = "convention.prefer_identity_column_over_bigserial"
    code = "CVG014"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "bigserial"
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer identity column over bigserial",
                ),
            )


class PreferJsonbOverJson(linter.Checker):
    """Prefer jsonb over json."""

    name = "convention.prefer_jsonb_over_json"
    code = "CVG015"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (node.typeName.names[-1].sval == "json"):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer jsonb over json",
                ),
            )


class PreferBigIntOverInt(linter.Checker):
    """Prefer bigint over int."""

    name = "convention.prefer_bigint_over_int"
    code = "CVG016"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "int4"
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer bigint over int",
                ),
            )


class PreferBigIntOverSmallInt(linter.Checker):
    """Prefer bigint over smallint."""

    name = "convention.prefer_bigint_over_smallint"
    code = "CVG017"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "int2"
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer bigint over smallint",
                ),
            )
