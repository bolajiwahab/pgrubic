"""Test not in."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN026 import NotIn


@pytest.fixture(scope="module")
def not_in() -> core.BaseChecker:
    """Create an instance of NotIn."""
    core.add_set_locations_to_rule(NotIn)
    return NotIn()


@pytest.fixture
def lint_not_in(
    linter: core.Linter,
    not_in: core.BaseChecker,
) -> core.Linter:
    """Lint NotIn."""
    linter.checkers.add(not_in)

    return linter


def test_not_in_rule_code(
    not_in: core.BaseChecker,
) -> None:
    """Test not in rule code."""
    assert not_in.code == not_in.__module__.split(".")[-1]


def test_not_in_auto_fixable(
    not_in: core.BaseChecker,
) -> None:
    """Test not in auto fixable."""
    assert not_in.is_auto_fixable is False


def test_pass_in_clause(
    lint_not_in: core.Linter,
) -> None:
    """Test pass in clause."""
    sql_pass: str = "SELECT * FROM measurement WHERE city_id IN (1, 2, 3);"

    violations: core.ViolationMetric = lint_not_in.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_not_in(
    lint_not_in: core.Linter,
) -> None:
    """Test fail not in."""
    sql_fail: str = "SELECT * FROM measurement WHERE city_id NOT IN (1, 2, 3);"

    violations: core.ViolationMetric = lint_not_in.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_not_in_description(
    lint_not_in: core.Linter,
    not_in: core.BaseChecker,
) -> None:
    """Test not in description."""
    sql_fail: str = "SELECT * FROM measurement WHERE city_id NOT IN (1, 2, 3);"

    _: core.ViolationMetric = lint_not_in.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(not_in.violations),
        ).description
        == "NOT IN detected"
    )


def test_pass_noqa_not_in(
    lint_not_in: core.Linter,
) -> None:
    """Test pass noqa not in."""
    sql_pass_noqa: str = """
    -- noqa: GN026
    SELECT * FROM measurement WHERE city_id NOT IN (1, 2, 3);
    """

    violations: core.ViolationMetric = lint_not_in.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_not_in(
    lint_not_in: core.Linter,
) -> None:
    """Test fail noqa not in."""
    sql_fail_noqa: str = """
    -- noqa: GN021
    SELECT * FROM measurement WHERE city_id NOT IN (1, 2, 3);
    """

    violations: core.ViolationMetric = lint_not_in.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_not_in(
    lint_not_in: core.Linter,
) -> None:
    """Test pass general noqa not in."""
    sql_pass_noqa: str = """
    -- noqa
    SELECT * FROM measurement WHERE city_id NOT IN (1, 2, 3);
    """

    violations: core.ViolationMetric = lint_not_in.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
