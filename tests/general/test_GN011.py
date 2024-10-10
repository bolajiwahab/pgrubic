"""Test missing required column."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.core import config
from pgrubic.rules.general.GN011 import MissingRequiredColumn


@pytest.fixture(scope="module")
def missing_required_column() -> core.BaseChecker:
    """Create an instance of MissingRequiredColumn."""
    core.add_apply_fix_to_rule(MissingRequiredColumn)
    core.add_set_locations_to_rule(MissingRequiredColumn)
    return MissingRequiredColumn()


@pytest.fixture
def lint_missing_required_column(
    linter: core.Linter,
    missing_required_column: core.BaseChecker,
) -> core.Linter:
    """Lint MissingRequiredColumn."""
    missing_required_column.config.lint.fix = False
    missing_required_column.config.lint.required_columns = [
        config.Column(
            name="created_at",
            data_type="timestamptz",
        ),
    ]
    linter.checkers.add(missing_required_column)

    return linter


def test_missing_required_column_rule_code(
    missing_required_column: core.BaseChecker,
) -> None:
    """Test missing required column rule code."""
    assert (
        missing_required_column.code == missing_required_column.__module__.split(".")[-1]
    )


def test_missing_required_column_auto_fixable(
    missing_required_column: core.BaseChecker,
) -> None:
    """Test missing required column auto fixable."""
    assert missing_required_column.is_auto_fixable is True


def test_pass_no_columns_table(
    lint_missing_required_column: core.Linter,
) -> None:
    """Test fail missing required column."""
    sql_fail: str = "CREATE TABLE music ();"

    violations: core.ViolationMetric = lint_missing_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_specified_required_column(
    lint_missing_required_column: core.Linter,
) -> None:
    """Test pass specified required column."""
    sql_fail: str = "CREATE TABLE music (age int, created_at timestamptz);"

    violations: core.ViolationMetric = lint_missing_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_missing_required_column(
    lint_missing_required_column: core.Linter,
) -> None:
    """Test fail missing required column."""
    sql_fail: str = "CREATE TABLE music (age int)"

    violations: core.ViolationMetric = lint_missing_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_missing_required_column_description(
    lint_missing_required_column: core.Linter,
    missing_required_column: core.BaseChecker,
) -> None:
    """Test missing required column description."""
    sql_fail: str = "CREATE TABLE music (age int)"

    _: core.ViolationMetric = lint_missing_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(missing_required_column.violations),
        ).description
        == "Column `created_at` of type `timestamptz` is marked as required in config"
    )


def test_pass_noqa_missing_required_column(
    lint_missing_required_column: core.Linter,
) -> None:
    """Test pass noqa missing required column."""
    sql_pass_noqa: str = """
    -- noqa: GN011
    CREATE TABLE music (age int)
    """

    violations: core.ViolationMetric = lint_missing_required_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_missing_required_column(
    lint_missing_required_column: core.Linter,
) -> None:
    """Test fail noqa missing required column."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE music (age int)
    """

    violations: core.ViolationMetric = lint_missing_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_missing_required_column(
    lint_missing_required_column: core.Linter,
) -> None:
    """Test fail noqa missing required column."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE music (age int)
    """

    violations: core.ViolationMetric = lint_missing_required_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_missing_required_column(
    lint_missing_required_column: core.Linter,
    missing_required_column: core.BaseChecker,
) -> None:
    """Test fail fix missing required column."""
    sql_fail: str = "CREATE TABLE music (age int)"

    sql_fix: str = (
        "CREATE TABLE music (\n    age integer\n  , created_at timestamptz NOT NULL\n);"
    )

    missing_required_column.config.lint.fix = True

    violations: core.ViolationMetric = lint_missing_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
