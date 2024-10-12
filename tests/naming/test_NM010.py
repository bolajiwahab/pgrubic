"""Test non snake case identifier."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.naming.NM010 import NonSnakeCaseIdentifier


@pytest.fixture(scope="module")
def non_snake_case_identifier() -> core.BaseChecker:
    """Create an instance of non snake case identifier."""
    core.add_set_locations_to_rule(NonSnakeCaseIdentifier)
    return NonSnakeCaseIdentifier()


@pytest.fixture
def lint_non_snake_case_identifier(
    linter: core.Linter,
    non_snake_case_identifier: core.BaseChecker,
) -> core.Linter:
    """Lint non snake case identifier."""
    linter.checkers.add(non_snake_case_identifier)

    return linter


def test_non_snake_case_identifier_rule_code(
    non_snake_case_identifier: core.BaseChecker,
) -> None:
    """Test non snake case identifier rule code."""
    assert (
        non_snake_case_identifier.code
        == non_snake_case_identifier.__module__.split(".")[-1]
    )


def test_non_snake_case_identifier_auto_fixable(
    non_snake_case_identifier: core.BaseChecker,
) -> None:
    """Test non snake case identifier  auto fixable."""
    assert non_snake_case_identifier.is_auto_fixable is False


def test_pass_snake_case_identifier(
    lint_non_snake_case_identifier: core.Linter,
) -> None:
    """Test pass snake case identifier."""
    sql_pass: str = "CREATE TABLE tbl (col int);"

    violations: core.ViolationMetric = lint_non_snake_case_identifier.run(
        file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_non_snake_case_identifier(
    lint_non_snake_case_identifier: core.Linter,
) -> None:
    """Test fail non snake case identifier."""
    sql_fail: str = """CREATE TABLE "TblAge" (col int);"""

    violations: core.ViolationMetric = lint_non_snake_case_identifier.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_non_snake_case_identifier_description(
    lint_non_snake_case_identifier: core.Linter,
    non_snake_case_identifier: core.BaseChecker,
) -> None:
    """Test non snake case identifier  description."""
    sql_fail: str = """CREATE TABLE tbl ("Col" int);"""

    _: core.ViolationMetric = lint_non_snake_case_identifier.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(non_snake_case_identifier.violations),
        ).description
        == "Identifier `Col` should be in snake case"
    )


def test_pass_noqa_non_snake_case_identifier(
    lint_non_snake_case_identifier: core.Linter,
) -> None:
    """Test pass noqa non snake case identifier."""
    sql_pass_noqa: str = """
    -- noqa: NM010
    CREATE VIEW "tbL" AS SELECT * FROM tbl;
    """

    violations: core.ViolationMetric = lint_non_snake_case_identifier.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_non_snake_case_identifier(
    lint_non_snake_case_identifier: core.Linter,
) -> None:
    """Test fail noqa non snake case identifier."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE OR REPLACE FUNCTION "Asterisks"(n int)
    RETURNS SETOF text
    RETURN repeat('*', generate_series (1, n));
    """

    violations: core.ViolationMetric = lint_non_snake_case_identifier.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_non_snake_case_identifier(
    lint_non_snake_case_identifier: core.Linter,
) -> None:
    """Test pass noqa non snake case identifier."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE "MEasurement__2024_02" PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');
    """

    violations: core.ViolationMetric = lint_non_snake_case_identifier.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
