"""Test usage of timestamp without time zone."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.typing.TP001 import TimestampWithoutTimezone


@pytest.fixture(scope="module")
def timestamp_without_timezone() -> core.BaseChecker:
    """Create an instance of TimestampWithoutTimezone."""
    core.add_apply_fix_to_rule(TimestampWithoutTimezone)
    core.add_set_locations_to_rule(TimestampWithoutTimezone)
    return TimestampWithoutTimezone()


@pytest.fixture
def lint_timestamp_without_timezone(
    linter: core.Linter,
    timestamp_without_timezone: core.BaseChecker,
) -> core.Linter:
    """Lint TimestampWithoutTimezone."""
    timestamp_without_timezone.config.lint.fix = False
    linter.checkers.add(timestamp_without_timezone)

    return linter


def test_timestamp_without_timezone_rule_code(
    timestamp_without_timezone: core.BaseChecker,
) -> None:
    """Test timestamp without timezone rule code."""
    assert (
        timestamp_without_timezone.code
        == timestamp_without_timezone.__module__.split(".")[-1]
    )


def test_timestamp_without_timezone_auto_fixable(
    timestamp_without_timezone: core.BaseChecker,
) -> None:
    """Test timestamp without timezone auto fixable."""
    assert timestamp_without_timezone.is_auto_fixable is True


def test_pass_create_table_timestamp_with_timezone(
    lint_timestamp_without_timezone: core.Linter,
) -> None:
    """Test pass timestamp without timezone."""
    sql_fail: str = "CREATE TABLE music (created_at timestamptz);"

    violations: core.ViolationMetric = lint_timestamp_without_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_timestamp_with_timezone(
    lint_timestamp_without_timezone: core.Linter,
) -> None:
    """Test pass timestamp without timezone."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timestamptz;"

    violations: core.ViolationMetric = lint_timestamp_without_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_timestamp_without_timezone(
    lint_timestamp_without_timezone: core.Linter,
) -> None:
    """Test fail create table timestamp without timezone."""
    sql_fail: str = "CREATE TABLE music (created_at timestamp);"

    violations: core.ViolationMetric = lint_timestamp_without_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_timestamp_without_timezone(
    lint_timestamp_without_timezone: core.Linter,
) -> None:
    """Test fail alter table timestamp without timezone."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timestamp(0);"

    violations: core.ViolationMetric = lint_timestamp_without_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_timestamp_without_timezone_description(
    lint_timestamp_without_timezone: core.Linter,
    timestamp_without_timezone: core.BaseChecker,
) -> None:
    """Test timestamp without timezone description."""
    sql_fail: str = "CREATE TABLE music (created_at timestamp);"

    _: core.ViolationMetric = lint_timestamp_without_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(timestamp_without_timezone.violations),
        ).description
        == "Prefer timestamp with timezone over timestamp without timezone"
    )


def test_pass_noqa_timestamp_without_timezone(
    lint_timestamp_without_timezone: core.Linter,
) -> None:
    """Test pass noqa timestamp without timezone."""
    sql_pass_noqa: str = """
    -- noqa: TP001
    CREATE TABLE music (age int, created_at timestamp(10))
    """

    violations: core.ViolationMetric = lint_timestamp_without_timezone.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_timestamp_without_timezone(
    lint_timestamp_without_timezone: core.Linter,
) -> None:
    """Test fail noqa timestamp without timezone."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE music ADD COLUMN created_at timestamp;
    """

    violations: core.ViolationMetric = lint_timestamp_without_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_timestamp_without_timezone(
    lint_timestamp_without_timezone: core.Linter,
) -> None:
    """Test pass noqa timestamp without timezone."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE music (age int, created_at timestamp);
    """

    violations: core.ViolationMetric = lint_timestamp_without_timezone.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_timestamp_without_timezone(
    lint_timestamp_without_timezone: core.Linter,
    timestamp_without_timezone: core.BaseChecker,
) -> None:
    """Test fail fix timestamp without timezone."""
    sql_fail: str = "CREATE TABLE music (age int, created_at timestamp);"

    sql_fix: str = "CREATE TABLE music (\n    age integer\n  , created_at timestamptz\n);"

    timestamp_without_timezone.config.lint.fix = True

    violations: core.ViolationMetric = lint_timestamp_without_timezone.run(
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


def test_fail_fix_alter_table_timestamp_without_timezone(
    lint_timestamp_without_timezone: core.Linter,
    timestamp_without_timezone: core.BaseChecker,
) -> None:
    """Test fail fix timestamp without timezone."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timestamp(0);"

    sql_fix: str = "ALTER TABLE music\n    ADD COLUMN created_at timestamptz;"

    timestamp_without_timezone.config.lint.fix = True

    violations: core.ViolationMetric = lint_timestamp_without_timezone.run(
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
