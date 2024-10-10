"""Test timestamp column without suffix."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.naming.NM015 import TimestampColumnWithoutSuffix


@pytest.fixture(scope="module")
def timestamp_column_without_suffix() -> core.BaseChecker:
    """Create an instance of timestamp column without suffix."""
    core.add_apply_fix_to_rule(TimestampColumnWithoutSuffix)
    core.add_set_locations_to_rule(TimestampColumnWithoutSuffix)
    return TimestampColumnWithoutSuffix()


@pytest.fixture
def lint_timestamp_column_without_suffix(
    linter: core.Linter,
    timestamp_column_without_suffix: core.BaseChecker,
) -> core.Linter:
    """Lint timestamp column without suffix."""
    timestamp_column_without_suffix.config.lint.fix = False
    timestamp_column_without_suffix.config.lint.timestamp_column_suffix = "_at"
    linter.checkers.add(timestamp_column_without_suffix)

    return linter


def test_timestamp_column_without_suffix_rule_code(
    timestamp_column_without_suffix: core.BaseChecker,
) -> None:
    """Test timestamp column without suffix rule code."""
    assert (
        timestamp_column_without_suffix.code
        == timestamp_column_without_suffix.__module__.split(".")[-1]
    )


def test_timestamp_column_without_suffix_auto_fixable(
    timestamp_column_without_suffix: core.BaseChecker,
) -> None:
    """Test timestamp column without suffix auto fixable."""
    assert timestamp_column_without_suffix.is_auto_fixable is True


def test_pass_non_timestamp_column_without_suffix(
    lint_timestamp_column_without_suffix: core.Linter,
) -> None:
    """Test pass non timestamp column without suffix."""
    sql_fail: str = "CREATE TABLE tbl (activated boolean);"

    violations: core.ViolationMetric = lint_timestamp_column_without_suffix.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_timestamp_column_without_suffix(
    lint_timestamp_column_without_suffix: core.Linter,
) -> None:
    """Test fail timestamp column without suffix."""
    sql_fail: str = "CREATE TABLE tbl (activated timestamp);"

    violations: core.ViolationMetric = lint_timestamp_column_without_suffix.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_timestamp_column_without_suffix_description(
    lint_timestamp_column_without_suffix: core.Linter,
    timestamp_column_without_suffix: core.BaseChecker,
) -> None:
    """Test timestamp column without suffix description."""
    sql_fail: str = "CREATE TABLE tbl (activated timestamp);"

    _: core.ViolationMetric = lint_timestamp_column_without_suffix.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(timestamp_column_without_suffix.violations),
        ).description
        == f"Timestamp column name should be suffixed with `{timestamp_column_without_suffix.config.lint.timestamp_column_suffix}`"  # noqa: E501
    )


def test_pass_noqa_timestamp_column_without_suffix(
    lint_timestamp_column_without_suffix: core.Linter,
) -> None:
    """Test pass noqa timestamp column without suffix."""
    sql_pass_noqa: str = """
    -- noqa: NM015
    CREATE TABLE tbl (activated timestamptz);
    """

    violations: core.ViolationMetric = lint_timestamp_column_without_suffix.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_timestamp_column_without_suffix(
    lint_timestamp_column_without_suffix: core.Linter,
) -> None:
    """Test fail noqa timestamp column without suffix."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN activated timestamp;
    """

    violations: core.ViolationMetric = lint_timestamp_column_without_suffix.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_timestamp_column_without_suffix(
    lint_timestamp_column_without_suffix: core.Linter,
) -> None:
    """Test pass noqa timestamp column without suffix."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (activated timestamp);
    """

    violations: core.ViolationMetric = lint_timestamp_column_without_suffix.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_timestamp_column_without_suffix(
    lint_timestamp_column_without_suffix: core.Linter,
    timestamp_column_without_suffix: core.BaseChecker,
) -> None:
    """Test fail fix timestamp column without suffix."""
    sql_fail: str = "CREATE TABLE tbl (activated timestamp);"

    sql_fix: str = "CREATE TABLE tbl (\n    activated_at timestamp\n);"

    timestamp_column_without_suffix.config.lint.fix = True

    violations: core.ViolationMetric = lint_timestamp_column_without_suffix.run(
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
