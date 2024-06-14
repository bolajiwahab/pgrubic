"""Convention for typing."""

from pglast import ast  # type: ignore[import-untyped]

from pgshield.core import linter


class PreferTimestampWithTimezoneOverTimestampWithoutTimezone(linter.Checker):
    """Prefer timestamp with timezone over timestamp without timezone."""

    name = "convention.prefer_timestamp_with_timezone_over_timestamp_without_timezone"
    code = "CVT001"

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        statement_index: int = linter.get_statement_index(ancestors)

        if (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors) and (
            node.typeName.names[-1].sval == "timestamp"
        ):

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer timestamp with timezone over timestamp without timezone",  # noqa: E501
                ),
            )


class PreferTimestampWithTimezoneOverTimeWithTimezone(linter.Checker):
    """Prefer timestamp with timezone over time with timezone."""

    name = "convention.prefer_timestamp_with_timezone_over_time_with_timezone"
    code = "CVT002"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer timestamp with timezone over time with timezone",  # noqa: E501
                ),
            )


class PreferEntireTimestampWithoutTimezone(linter.Checker):
    """Prefer entire timestamp without timezone."""

    name = "convention.prefer_entire_timestamp_without_timezone"
    code = "CVT003"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer entire timestamp without timezone",
                ),
            )


class PreferEntireTimestampWithTimezone(linter.Checker):
    """Prefer entire timestamp with timezone."""

    name = "convention.prefer_entire_timestamp_with_timezone"
    code = "CVT004"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer entire timestamp with timezone",
                ),
            )


class PreferTextOverChar(linter.Checker):
    """Prefer text over char."""

    name = "convention.prefer_text_over_char"
    code = "CVT005"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer text over char",
                ),
            )


class PreferTextOverVarChar(linter.Checker):
    """Prefer text over varchar."""

    name = "convention.prefer_text_over_var_char"
    code = "CVT006"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer text over varchar",
                ),
            )


class PreferNumericOverMoney(linter.Checker):
    """Prefer numeric over money."""

    name = "convention.prefer_numeric_over_money"
    code = "CVT007"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer numeric over money",
                ),
            )


class PreferIdentityColumnOverSerial(linter.Checker):
    """Prefer identity column over serial."""

    name = "convention.prefer_identity_column_over_serial"
    code = "CVT008"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer identity column over serial",
                ),
            )


class PreferIdentityColumnOverBigSerial(linter.Checker):
    """Prefer identity column over bigserial."""

    name = "convention.prefer_identity_column_over_bigserial"
    code = "CVT009"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer identity column over bigserial",
                ),
            )


class PreferJsonbOverJson(linter.Checker):
    """Prefer jsonb over json."""

    name = "convention.prefer_jsonb_over_json"
    code = "CVT010"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer jsonb over json",
                ),
            )


class PreferBigIntOverInt(linter.Checker):
    """Prefer bigint over int."""

    name = "convention.prefer_bigint_over_int"
    code = "CVT011"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer bigint over int",
                ),
            )


class PreferBigIntOverSmallInt(linter.Checker):
    """Prefer bigint over smallint."""

    name = "convention.prefer_bigint_over_smallint"
    code = "CVT012"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer bigint over smallint",
                ),
            )


class WronglyTypedRequiredColumn(linter.Checker):
    """Wrongly typed required column."""

    name = "convention.wrongly_typed_required_column"
    code = "CVT013"

    def visit_ColumnDef(
    self,
    ancestors: ast.Node,
    node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors)
            and node.colname in self.config.required_columns
            and node.typeName.names[-1].sval != self.config.required_columns[node.colname]  # noqa: E501
        ):

            statement_index: int = linter.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description=f"Column '{node.colname}' expected type is"
                                f" '{self.config.required_columns[node.colname]}',"
                                f" found '{node.typeName.names[-1].sval}'",
                ),
            )


class BlacklistedType(linter.Checker):
    """Blacklisted type."""

    name = "convention.blacklisted_type"
    code = "CVT014"

    def visit_ColumnDef(
    self,
    ancestors: ast.Node,
    node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            (ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors)
            and node.typeName.names[-1].sval in self.config.blacklisted_types
        ):

            statement_index: int = linter.get_statement_index(ancestors)

            self.violations.append(
                linter.Violation(
                    lineno=ancestors[statement_index].stmt_location,
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description=f"Type '{node.typeName.names[-1].sval}' is blacklisted",
                ),
            )


class PreferIdentityColumnOverSmallSerial(linter.Checker):
    """Prefer identity column over smallserial."""

    name = "convention.prefer_identity_column_over_smallserial"
    code = "CVT015"

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
                    column_offset=node.location,
                    statement=ancestors[statement_index],
                    description="Prefer identity column over smallserial",
                ),
            )

# contents[:loc].count('\n') + 1
# line_end = contents.find('\n', loc)
