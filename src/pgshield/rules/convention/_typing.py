"""Convention for typing."""

from pglast import ast

from pgshield import SCHEMA_QUALIFIED_TYPE
from pgshield.core import linter


def _is_column_creation(ancestors: ast.Node) -> bool:
    """Check ancestors for column creation."""
    return ast.CreateStmt in ancestors or ast.AlterTableCmd in ancestors


class PreferTextOverVarchar(linter.Checker):
    """Prefer text over varchar."""

    name: str = "convention.prefer_text_over_varchar"
    code: str = "TYP006"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (
            node.typeName.names[-1].sval == "varchar"
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer text over varchar",
                ),
            )


class PreferNumericOverMoney(linter.Checker):
    """Prefer numeric over money."""

    name: str = "convention.prefer_numeric_over_money"
    code: str = "TYP007"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (node.typeName.names[-1].sval == "money"):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer numeric over money",
                ),
            )


class PreferIdentityColumnOverSerial(linter.Checker):
    """Prefer identity column over serial."""

    name: str = "convention.prefer_identity_column_over_serial"
    code: str = "TYP008"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (
            node.typeName.names[-1].sval == "serial"
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer identity column over serial",
                ),
            )


class PreferIdentityColumnOverBigSerial(linter.Checker):
    """Prefer identity column over bigserial."""

    name: str = "convention.prefer_identity_column_over_bigserial"
    code: str = "TYP009"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (
            node.typeName.names[-1].sval == "bigserial"
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer identity column over bigserial",
                ),
            )


class PreferJsonbOverJson(linter.Checker):
    """Prefer jsonb over json."""

    name: str = "convention.prefer_jsonb_over_json"
    code: str = "TYP010"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (node.typeName.names[-1].sval == "json"):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer jsonb over json",
                ),
            )


class PreferBigIntOverInt(linter.Checker):
    """Prefer bigint over int."""

    name: str = "convention.prefer_bigint_over_int"
    code: str = "TYP011"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (node.typeName.names[-1].sval == "int4"):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer bigint over int",
                ),
            )


class PreferBigIntOverSmallInt(linter.Checker):
    """Prefer bigint over smallint."""

    name: str = "convention.prefer_bigint_over_smallint"
    code: str = "TYP012"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (node.typeName.names[-1].sval == "int2"):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer bigint over smallint",
                ),
            )


class WronglyTypedRequiredColumn(linter.Checker):
    """Wrongly typed required column."""

    name: str = "convention.wrongly_typed_required_column"
    code: str = "TYP013"

    is_auto_fixable = True

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if (
            _is_column_creation(ancestors)
            and node.colname in self.config.required_columns
            and node.typeName.names[-1].sval
            != self.config.required_columns[node.colname]
        ):

            given_type = ".".join(a.sval for a in node.typeName.names)

            expected_type = self.config.required_columns[node.colname].split(".")

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Column '{node.colname}' expected type is"
                    f" '{self.config.required_columns[node.colname]}',"
                    f" found '{given_type}'",
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

    name: str = "convention.blacklisted_type"
    code: str = "TYP014"

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

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description=f"Type '{node.typeName.names[-1].sval}' is blacklisted",
                ),
            )


class PreferIdentityColumnOverSmallSerial(linter.Checker):
    """Prefer identity column over smallserial."""

    name: str = "convention.prefer_identity_column_over_smallserial"
    code: str = "TYP015"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (
            node.typeName.names[-1].sval == "smallserial"
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer identity column over smallserial",
                ),
            )


class PreferJsonbOverHstore(linter.Checker):
    """Prefer jsonb over hstore."""

    name: str = "convention.prefer_jsonb_over_hstore"
    code: str = "TYP016"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (
            node.typeName.names[-1].sval == "hstore"
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer jsonb over hstore",
                ),
            )


class PreferJsonbOverXml(linter.Checker):
    """Prefer jsonb over xml."""

    name: str = "convention.prefer_jsonb_over_xml"
    code: str = "TYP017"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (node.typeName.names[-1].sval == "xml"):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer jsonb over xml",
                ),
            )


class PreferNumericOverFloat(linter.Checker):
    """Prefer numeric over float."""

    name: str = "convention.prefer_numeric_over_float"
    code: str = "TYP018"

    is_auto_fixable: bool = False

    def visit_ColumnDef(
        self,
        ancestors: ast.Node,
        node: ast.ColumnDef,
    ) -> None:
        """Visit ColumnDef."""
        if _is_column_creation(ancestors) and (
            node.typeName.names[-1].sval == "float8"
        ):

            self.violations.append(
                linter.Violation(
                    statement_location=self.statement_location,
                    statement_length=self.statement_length,
                    node_location=self.node_location,
                    description="Prefer numeric over float",
                ),
            )
