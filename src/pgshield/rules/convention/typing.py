"""Convention for typing."""

from pglast import ast

from pgshield import SCHEMA_QUALIFIED_TYPE, system_types
from pgshield.core import linter


class PreferTimestampWithTimezoneOverTimestampWithoutTimezone(linter.Checker):
    """Prefer timestamp with timezone over timestamp without timezone."""

    name = "convention.prefer_timestamp_with_timezone_over_timestamp_without_timezone"
    code = "CVT001"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "timestamp"
            and node.typeName.names[0].sval == "pg_catalog"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer timestamp with timezone over timestamp without timezone",  # noqa: E501
                ),
            )

            if self.config.fix is True:

                node.typeName.names[-1].sval = "timestamptz"


class PreferTimestampWithTimezoneOverTimeWithTimezone(linter.Checker):
    """Prefer timestamp with timezone over time with timezone."""

    name = "convention.prefer_timestamp_with_timezone_over_time_with_timezone"
    code = "CVT002"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "timetz"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer timestamp with timezone over time with timezone",  # noqa: E501
                ),
            )


class PreferEntireTimestampWithoutTimezone(linter.Checker):
    """Prefer entire timestamp without timezone."""

    name = "convention.prefer_entire_timestamp_without_timezone"
    code = "CVT003"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "timestamp" and node.typeName.typmods
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer entire timestamp without timezone",
                ),
            )


class PreferEntireTimestampWithTimezone(linter.Checker):
    """Prefer entire timestamp with timezone."""

    name = "convention.prefer_entire_timestamp_with_timezone"
    code = "CVT004"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "timestamptz" and node.typeName.typmods
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer entire timestamp with timezone",
                ),
            )


class PreferTextOverChar(linter.Checker):
    """Prefer text over char."""

    name = "convention.prefer_text_over_char"
    code = "CVT005"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval in ["bpchar", "char"]
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer text over char",
                ),
            )


class PreferTextOverVarchar(linter.Checker):
    """Prefer text over varchar."""

    name = "convention.prefer_text_over_varchar"
    code = "CVT006"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "varchar"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer text over varchar",
                ),
            )


class PreferNumericOverMoney(linter.Checker):
    """Prefer numeric over money."""

    name = "convention.prefer_numeric_over_money"
    code = "CVT007"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "money"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer numeric over money",
                ),
            )


class PreferIdentityColumnOverSerial(linter.Checker):
    """Prefer identity column over serial."""

    name = "convention.prefer_identity_column_over_serial"
    code = "CVT008"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "serial"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer identity column over serial",
                ),
            )


class PreferIdentityColumnOverBigSerial(linter.Checker):
    """Prefer identity column over bigserial."""

    name = "convention.prefer_identity_column_over_bigserial"
    code = "CVT009"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "bigserial"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer identity column over bigserial",
                ),
            )


class PreferJsonbOverJson(linter.Checker):
    """Prefer jsonb over json."""

    name = "convention.prefer_jsonb_over_json"
    code = "CVT010"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "json"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer jsonb over json",
                ),
            )


class PreferBigIntOverInt(linter.Checker):
    """Prefer bigint over int."""

    name = "convention.prefer_bigint_over_int"
    code = "CVT011"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "int4"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer bigint over int",
                ),
            )


class PreferBigIntOverSmallInt(linter.Checker):
    """Prefer bigint over smallint."""

    name = "convention.prefer_bigint_over_smallint"
    code = "CVT012"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "int2"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer bigint over smallint",
                ),
            )


class WronglyTypedRequiredColumn(linter.Checker):
    """Wrongly typed required column."""

    name = "convention.wrongly_typed_required_column"
    code = "CVT013"

    is_auto_fixable = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors)
            and node.colname in self.config.required_columns
            and ".".join(a.sval for a in node.typeName.names)
            != system_types.get(
                self.config.required_columns[node.colname],
                self.config.required_columns[node.colname],
            )
        ):

            expected_type = system_types.get(
                self.config.required_columns[node.colname],
                self.config.required_columns[node.colname],
            ).split(".")

            given_type = ".".join(a.sval for a in node.typeName.names)

            statement_index: int = linter.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    statement_location=ancestors[statement_index].stmt_location,
                    statement_length=ancestors[statement_index].stmt_len,
                    column_offset=linter.get_column_offset(ancestors, node),
                    # statement=ancestors[statement_index],
                    description=f"Column '{node.colname}' expected type is"
                    f" '{self.config.required_columns[node.colname]}',"
                    f" found '{system_types.get(given_type, given_type)}'",
                ),
            )

            if (
                self.config.fix is True
                and len(node.typeName.names) == SCHEMA_QUALIFIED_TYPE
                and len(expected_type) == SCHEMA_QUALIFIED_TYPE
            ):

                node.typeName.names[0].sval = expected_type[0]
                node.typeName.names[1].sval = expected_type[1]


class BlacklistedType(linter.Checker):
    """Blacklisted type."""

    name = "convention.blacklisted_type"
    code = "CVT014"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors
        ) and node.typeName.names[-1].sval in self.config.blacklisted_types:

            statement_index: int = linter.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description=f"Type '{node.typeName.names[-1].sval}' is blacklisted",
                ),
            )


class PreferIdentityColumnOverSmallSerial(linter.Checker):
    """Prefer identity column over smallserial."""

    name = "convention.prefer_identity_column_over_smallserial"
    code = "CVT015"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "smallserial"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer identity column over smallserial",
                ),
            )


class PreferJsonbOverHstore(linter.Checker):
    """Prefer jsonb over hstore."""

    name = "convention.prefer_jsonb_over_hstore"
    code = "CVT016"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "hstore"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer jsonb over hstore",
                ),
            )


class PreferJsonbOverXml(linter.Checker):
    """Prefer jsonb over xml."""

    name = "convention.prefer_jsonb_over_xml"
    code = "CVT017"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "xml"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=linter.get_column_offset(ancestors, node),
                    statement=ancestors[statement_index],
                    description="Prefer jsonb over xml",
                ),
            )
