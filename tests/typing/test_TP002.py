"""Test usage of time with time zone."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.typing.TP002 import TimeWithTimeZone


@pytest.fixture(scope="module")
def time_with_timezone() -> core.BaseChecker:
    """Create an instance of TimeWithTimeZone."""
    core.add_apply_fix_to_rule(TimeWithTimeZone)
    core.add_set_locations_to_rule(TimeWithTimeZone)
    return TimeWithTimeZone()


@pytest.fixture
def lint_time_with_timezone(
    linter: core.Linter,
    time_with_timezone: core.BaseChecker,
) -> core.Linter:
    """Lint TimeWithTimeZone."""
    time_with_timezone.config.lint.fix = False
    linter.checkers.add(time_with_timezone)

    return linter


def test_time_with_timezone_rule_code(
    time_with_timezone: core.BaseChecker,
) -> None:
    """Test time with timezone rule code."""
    assert time_with_timezone.code == time_with_timezone.__module__.split(".")[-1]


def test_time_with_timezone_auto_fixable(
    time_with_timezone: core.BaseChecker,
) -> None:
    """Test time with timezone auto fixable."""
    assert time_with_timezone.is_auto_fixable is True


def test_pass_create_table_timestamp_with_timezone(
    lint_time_with_timezone: core.Linter,
) -> None:
    """Test pass time with timezone."""
    sql_fail: str = "CREATE TABLE music (created_at timestamptz);"

    violations: core.ViolationMetric = lint_time_with_timezone.run(
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
    lint_time_with_timezone: core.Linter,
) -> None:
    """Test pass time with timezone."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timestamptz;"

    violations: core.ViolationMetric = lint_time_with_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_time_with_timezone(
    lint_time_with_timezone: core.Linter,
) -> None:
    """Test fail create table time with timezone."""
    sql_fail: str = "CREATE TABLE music (created_at timetz);"

    violations: core.ViolationMetric = lint_time_with_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_time_with_timezone(
    lint_time_with_timezone: core.Linter,
) -> None:
    """Test fail alter table time with timezone."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timetz;"

    violations: core.ViolationMetric = lint_time_with_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_time_with_timezone_description(
    lint_time_with_timezone: core.Linter,
    time_with_timezone: core.BaseChecker,
) -> None:
    """Test time with timezone description."""
    sql_fail: str = "CREATE TABLE music (created_at timetz);"

    _: core.ViolationMetric = lint_time_with_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(time_with_timezone.violations),
        ).description
        == "Prefer timestamp with timezone over time with timezone"
    )


def test_pass_noqa_time_with_timezone(
    lint_time_with_timezone: core.Linter,
) -> None:
    """Test pass noqa time with timezone."""
    sql_pass_noqa: str = """
    -- noqa: TP002
    CREATE TABLE music (age int, created_at timetz)
    """

    violations: core.ViolationMetric = lint_time_with_timezone.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_time_with_timezone(
    lint_time_with_timezone: core.Linter,
) -> None:
    """Test fail noqa time with timezone."""
    sql_fail_noqa: str = """
    -- noqa: TP001
    ALTER TABLE music ADD COLUMN created_at timetz;
    """

    violations: core.ViolationMetric = lint_time_with_timezone.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_time_with_timezone(
    lint_time_with_timezone: core.Linter,
) -> None:
    """Test pass noqa time with timezone."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE music (age int, created_at timetz);
    """

    violations: core.ViolationMetric = lint_time_with_timezone.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_time_with_timezone(
    lint_time_with_timezone: core.Linter,
    time_with_timezone: core.BaseChecker,
) -> None:
    """Test fail fix time with timezone."""
    sql_fail: str = "CREATE TABLE music (age int, created_at timetz);"

    sql_fix: str = "CREATE TABLE music (\n    age integer\n  , created_at timestamptz\n);"

    time_with_timezone.config.lint.fix = True

    violations: core.ViolationMetric = lint_time_with_timezone.run(
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


def test_fail_fix_alter_table_time_with_timezone(
    lint_time_with_timezone: core.Linter,
    time_with_timezone: core.BaseChecker,
) -> None:
    """Test fail fix time with timezone."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timetz;"

    sql_fix: str = "ALTER TABLE music\n    ADD COLUMN created_at timestamptz;"

    time_with_timezone.config.lint.fix = True

    violations: core.ViolationMetric = lint_time_with_timezone.run(
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
