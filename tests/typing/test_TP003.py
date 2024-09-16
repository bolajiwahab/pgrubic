"""Test for usage of timestamp with time zone with precision."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.typing.TP003 import TimestampWithTimezoneWithPrecision


@pytest.fixture(scope="module")
def timestamp_with_timezone_with_precision() -> core.BaseChecker:
    """Create an instance of TimestampWithTimezoneWithPrecision."""
    core.add_apply_fix_to_rule(TimestampWithTimezoneWithPrecision)
    core.add_set_locations_to_rule(TimestampWithTimezoneWithPrecision)
    return TimestampWithTimezoneWithPrecision()


@pytest.fixture
def lint_timestamp_with_timezone_with_precision(
    linter: core.Linter,
    timestamp_with_timezone_with_precision: core.BaseChecker,
) -> core.Linter:
    """Lint TimestampWithTimezoneWithPrecision."""
    timestamp_with_timezone_with_precision.config.lint.fix = False
    linter.checkers.add(timestamp_with_timezone_with_precision)

    return linter


def test_timestamp_with_timezone_with_precision_rule_code(
    timestamp_with_timezone_with_precision: core.BaseChecker,
) -> None:
    """Test timestamp with timezone with precision rule code."""
    assert (
        timestamp_with_timezone_with_precision.code
        == timestamp_with_timezone_with_precision.__module__.split(".")[-1]
    )


def test_timestamp_with_timezone_with_precision_auto_fixable(
    timestamp_with_timezone_with_precision: core.BaseChecker,
) -> None:
    """Test timestamp with timezone with precision auto fixable."""
    assert timestamp_with_timezone_with_precision.is_auto_fixable is True


def test_pass_create_table_timestamp_with_timezone(
    lint_timestamp_with_timezone_with_precision: core.Linter,
) -> None:
    """Test pass timestamp with timezone with precision."""
    sql_fail: str = "CREATE TABLE music (created_at timestamptz);"

    violations: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_timestamp_with_timezone(
    lint_timestamp_with_timezone_with_precision: core.Linter,
) -> None:
    """Test pass timestamp with timezone with precision."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timestamptz;"

    violations: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_timestamp_with_timezone_with_precision(
    lint_timestamp_with_timezone_with_precision: core.Linter,
) -> None:
    """Test fail create table timestamp with timezone with precision."""
    sql_fail: str = "CREATE TABLE music (created_at timestamptz(0));"

    violations: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_timestamp_with_timezone_with_precision(
    lint_timestamp_with_timezone_with_precision: core.Linter,
) -> None:
    """Test fail alter table timestamp with timezone with precision."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timestamptz(0);"

    violations: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_timestamp_with_timezone_with_precision_description(
    lint_timestamp_with_timezone_with_precision: core.Linter,
    timestamp_with_timezone_with_precision: core.BaseChecker,
) -> None:
    """Test timestamp with timezone with precision description."""
    sql_fail: str = "CREATE TABLE music (created_at timestamptz(0));"

    _: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(timestamp_with_timezone_with_precision.violations),
        ).description
        == "Prefer entire timestamp with timezone"
    )


def test_pass_noqa_timestamp_with_timezone_with_precision(
    lint_timestamp_with_timezone_with_precision: core.Linter,
) -> None:
    """Test pass noqa timestamp with timezone with precision."""
    sql_pass_noqa: str = """
    -- noqa: TP003
    CREATE TABLE music (age int, created_at timestamptz(10))
    """

    violations: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_timestamp_with_timezone_with_precision(
    lint_timestamp_with_timezone_with_precision: core.Linter,
) -> None:
    """Test fail noqa timestamp with timezone with precision."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE music ADD COLUMN created_at timestamptz(0);
    """

    violations: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_timestamp_with_timezone_with_precision(
    lint_timestamp_with_timezone_with_precision: core.Linter,
) -> None:
    """Test pass noqa timestamp with timezone with precision."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE music (age int, created_at timestamptz(0));
    """

    violations: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_timestamp_with_timezone_with_precision(
    lint_timestamp_with_timezone_with_precision: core.Linter,
    timestamp_with_timezone_with_precision: core.BaseChecker,
) -> None:
    """Test fail fix timestamp with timezone with precision."""
    sql_fail: str = "CREATE TABLE music (age int, created_at timestamptz(0));"

    sql_fix: str = (
        "CREATE TABLE music (\n    age integer\n  , created_at timestamptz\n);"
    )

    timestamp_with_timezone_with_precision.config.lint.fix = True

    violations: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_timestamp_with_timezone_with_precision(
    lint_timestamp_with_timezone_with_precision: core.Linter,
    timestamp_with_timezone_with_precision: core.BaseChecker,
) -> None:
    """Test fail fix timestamp with timezone with precision."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timestamptz(0);"

    sql_fix: str = "ALTER TABLE music\n    ADD COLUMN created_at timestamptz;"

    timestamp_with_timezone_with_precision.config.lint.fix = True

    violations: core.ViolationMetric = lint_timestamp_with_timezone_with_precision.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
