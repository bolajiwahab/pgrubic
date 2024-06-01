"""Rules for convention."""

# blacklist
# creation
import re

from pglast import ast, enums, stream  # type: ignore[import-untyped]

from pgshield import utils, linter


class NoSQLASCIIEncoding(linter.Checker):  # type: ignore[misc]
    """No table inheritance."""

    name = "convention.no_sql_ascii_encoding"
    code = "COV001"

    def visit_CreatedbStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreatedbStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

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
    code = "COV002"

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            node.inhRelations
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
    code = "COV003"

    def visit_RuleStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,  # noqa: ARG002
    ) -> None:
        """Visit RuleStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

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


class NoUpperCaseNameForTable(linter.Checker):  # type: ignore[misc]
    """No upper case name for table."""

    name = "convention.no_upper_case_name_for_table"
    code = "COV004"

    def visit_CreateStmt(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit CreateStmt."""
        statement_index: int = utils.get_statement_index(ancestors)

        if (
            any(ele.isupper() for ele in node.relation.relname)
            and (ancestors[statement_index].stmt_location, self.code)
            not in self.ignore_rules
        ):

            self.violations.append(
                linter.Violation(
                    location=ancestors[statement_index].stmt_location,
                    statement=ancestors[statement_index],
                    description="Upper case name for table",
                ),
            )


class NoUpperCaseNameForColumn(linter.Checker):  # type: ignore[misc]
    """No upper case name for column."""

    name = "convention.no_upper_case_name_for_column"
    code = "COV005"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        if ast.CreateStmt in ancestors:

            statement_index: int = utils.get_statement_index(ancestors)

            if (
                any(ele.isupper() for ele in node.colname)
                and (ancestors[statement_index].stmt_location, self.code)
                not in self.ignore_rules
            ):

                self.violations.append(
                    linter.Violation(
                        location=ancestors[statement_index].stmt_location,
                        statement=ancestors[statement_index],
                        description="Upper case name for column",
                    ),
                )


class TimestampWithoutTimezone(linter.Checker):  # type: ignore[misc]
    """Timestamp without timezone."""

    name = "convention.timestamp_without_timezone"
    code = "COV006"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors:

            data_types = (
                [stream.RawStream()(data_type) for data_type in node.typeName.names]
                if node.typeName.names is not None
                else []
            )

            if (
                any(dt.strip("'") == "timestamp" for dt in data_types)
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
    code = "COV007"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors:

            data_types = (
                [
                    stream.RawStream()(data_type).strip("'")
                    for data_type in node.typeName.names
                ]
                if node.typeName.names is not None
                else []
            )

            if (
                any(dt == "timetz" for dt in data_types)
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
    code = "COV008"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors:

            data_types = (
                [
                    stream.RawStream()(data_type).strip("'")
                    for data_type in node.typeName.names
                ]
                if node.typeName.names is not None
                else []
            )

            if (
                any(dt == "timestamp" for dt in data_types)
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
    code = "COV009"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors:

            data_types = (
                [
                    stream.RawStream()(data_type).strip("'")
                    for data_type in node.typeName.names
                ]
                if node.typeName.names is not None
                else []
            )

            if (
                any(dt == "timestamptz" for dt in data_types)
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
    code = "COV010"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors:

            data_types = (
                [
                    stream.RawStream()(data_type).strip("'")
                    for data_type in node.typeName.names
                ]
                if node.typeName.names is not None
                else []
            )

            if (
                any(dt == "bpchar" for dt in data_types)
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
    code = "COV011"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors:

            data_types = (
                [
                    stream.RawStream()(data_type).strip("'")
                    for data_type in node.typeName.names
                ]
                if node.typeName.names is not None
                else []
            )

            if (
                any(dt == "varchar" for dt in data_types)
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
    code = "COV012"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors:

            data_types = (
                [
                    stream.RawStream()(data_type).strip("'")
                    for data_type in node.typeName.names
                ]
                if node.typeName.names is not None
                else []
            )

            if (
                any(dt == "money" for dt in data_types)
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
    code = "COV013"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors:

            data_types = (
                [
                    stream.RawStream()(data_type).strip("'")
                    for data_type in node.typeName.names
                ]
                if node.typeName.names is not None
                else []
            )

            if (
                any(dt == "serial" for dt in data_types)
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
    code = "COV014"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.Node,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = utils.get_statement_index(ancestors)

        if ast.CreateStmt in ancestors:

            data_types = (
                [
                    stream.RawStream()(data_type).strip("'")
                    for data_type in node.typeName.names
                ]
                if node.typeName.names is not None
                else []
            )

            if (
                any(dt == "bigserial" for dt in data_types)
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
