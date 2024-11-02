"""Test current time."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN020 import CurrentTime


@pytest.fixture(scope="module")
def current_time() -> core.BaseChecker:
    """Create an instance of CurrentTime."""
    core.add_apply_fix_to_rule(CurrentTime)
    core.add_set_locations_to_rule(CurrentTime)
    return CurrentTime()


@pytest.fixture
def lint_current_time(
    linter: core.Linter,
    current_time: core.BaseChecker,
) -> core.Linter:
    """Lint CurrentTime."""
    current_time.config.lint.fix = False
    linter.checkers.add(current_time)

    return linter


def test_current_time_rule_code(
    current_time: core.BaseChecker,
) -> None:
    """Test current time rule code."""
    assert current_time.code == current_time.__module__.split(".")[-1]


def test_current_time_auto_fixable(
    current_time: core.BaseChecker,
) -> None:
    """Test current time auto fixable."""
    assert current_time.is_auto_fixable is True


def test_pass_current_timestamp(
    lint_current_time: core.Linter,
) -> None:
    """Test pass current time."""
    sql_pass: str = "SELECT CURRENT_TIMESTAMP;"

    violations: core.ViolationMetric = lint_current_time.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_current_time(
    lint_current_time: core.Linter,
) -> None:
    """Test fail current time."""
    sql_fail: str = "SELECT CURRENT_TIME;"

    violations: core.ViolationMetric = lint_current_time.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_current_time_description(
    lint_current_time: core.Linter,
    current_time: core.BaseChecker,
) -> None:
    """Test current time description."""
    sql_fail: str = "ALTER TABLE tbl ALTER COLUMN time SET DEFAULT CURRENT_TIME;"

    _: core.ViolationMetric = lint_current_time.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(current_time.violations),
        ).description
        == "Prefer functions that return timestamptz instead of timetz"
    )


def test_pass_noqa_current_time(
    lint_current_time: core.Linter,
) -> None:
    """Test pass noqa current time."""
    sql_pass_noqa: str = """
    -- noqa: GN020
    CREATE TABLE tbl (time time DEFAULT CURRENT_TIME);
    """

    violations: core.ViolationMetric = lint_current_time.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_current_time(
    lint_current_time: core.Linter,
) -> None:
    """Test fail noqa current time."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE tbl (time time DEFAULT CURRENT_TIME);
    """

    violations: core.ViolationMetric = lint_current_time.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_current_time(
    lint_current_time: core.Linter,
) -> None:
    """Test fail noqa current time."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE tbl (time time DEFAULT CURRENT_TIME);
    """

    violations: core.ViolationMetric = lint_current_time.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_current_time(
    lint_current_time: core.Linter,
    current_time: core.BaseChecker,
) -> None:
    """Test fail fix current time."""
    sql_fail: str = "CREATE TABLE tbl (time time DEFAULT CURRENT_TIME);"

    sql_fix: str = "CREATE TABLE tbl (\n    time time DEFAULT CURRENT_TIMESTAMP\n);\n"

    current_time.config.lint.fix = True

    violations: core.ViolationMetric = lint_current_time.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_current_time(
    lint_current_time: core.Linter,
    current_time: core.BaseChecker,
) -> None:
    """Test fail fix current time."""
    sql_fail: str = "ALTER TABLE account ALTER COLUMN time SET DEFAULT CURRENT_TIME;"

    sql_fix: str = (
        "ALTER TABLE account\n    ALTER COLUMN time SET DEFAULT CURRENT_TIMESTAMP;\n"
    )

    current_time.config.lint.fix = True

    violations: core.ViolationMetric = lint_current_time.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
