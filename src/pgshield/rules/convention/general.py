"""General convention."""

import re

from pglast import ast, stream  # type: ignore[import-untyped]

from pgshield.core import linter


class NoSQLASCIIEncoding(linter.Checker):  # type: ignore[misc]
    """No ascii encoding."""

    name = "convention.no_sql_ascii_encoding"
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

        if (
            options.get("encoding") == "sql_ascii"
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of sql_ascii encoding",
                ),
            )


class NoTableInheritance(linter.Checker):  # type: ignore[misc]
    """No table inheritance."""

    name = "convention.no_table_inheritance"
    code = "CVG002"

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.CreateStmt,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            node.inhRelations
            and not node.partbound
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of table inheritance, use declarative partitioning",  # noqa: E501
                ),
            )


class NoRule(linter.Checker):  # type: ignore[misc]
    """No rule."""

    name = "convention.no_rule"
    code = "CVG003"

    def visit_RuleStmt(
        self,
        ancestors: ast.Node,
        node: ast.RuleStmt,  # noqa: ARG002
    ) -> None:
        """Visit RuleStmt."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (
            ancestors[statement_index].stmt_location,
            self.code,
        ) not in self.ignore_rules:

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of rule, use trigger instead",
                ),
            )


class TimestampWithoutTimezone(linter.Checker):  # type: ignore[misc]
    """Timestamp without timezone."""

    name = "convention.timestamp_without_timezone"
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
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of timestamp without timezone",
                ),
            )


class TimeWithtTimezone(linter.Checker):  # type: ignore[misc]
    """Time with timezone."""

    name = "convention.time_with_timezone"
    code = "CVG007"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "timetz"
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of time with timezone",
                ),
            )


class TruncatedTimestampWithoutTimezone(linter.Checker):  # type: ignore[misc]
    """Truncated timestamp without timezone."""

    name = "convention.truncated_timestamp_without_timezone"
    code = "CVG008"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "timestamp"
            and node.typeName.typmods
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of truncated timestamp without timezone",
                ),
            )


class TruncatedTimestampWithTimezone(linter.Checker):  # type: ignore[misc]
    """Truncated timestamp with timezone."""

    name = "convention.truncated_timestamp_with_timezone"
    code = "CVG009"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "timestamptz"
            and node.typeName.typmods
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of truncated timestamp with timezone",
                ),
            )


class Char(linter.Checker):  # type: ignore[misc]
    """Char."""

    name = "convention.char"
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
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of char",
                ),
            )


class VarChar(linter.Checker):  # type: ignore[misc]
    """VarChar."""

    name = "convention.varchar"
    code = "CVG011"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "varchar"
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of varchar",
                ),
            )


class Money(linter.Checker):  # type: ignore[misc]
    """Money."""

    name = "convention.Money"
    code = "CVG012"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "money"
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of money",
                ),
            )


class Serial(linter.Checker):  # type: ignore[misc]
    """serial."""

    name = "convention.serial"
    code = "CVG013"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "serial"
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of serial",
                ),
            )


class BigSerial(linter.Checker):  # type: ignore[misc]
    """Bigserial."""

    name = "convention.bigserial"
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
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Usage of bigserial",
                ),
            )


class PreferJsonbOverJson(linter.Checker):  # type: ignore[misc]
    """PreferJsonbOverJson."""

    name = "convention.prefer_jsonb_over_json"
    code = "CVG015"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors and (
            node.typeName.names[-1].sval == "json"
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Prefer jsonb over json",
                ),
            )
