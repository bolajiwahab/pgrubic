"""Test a_star."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN029 import AStar


@pytest.fixture(scope="module")
def a_star() -> core.BaseChecker:
    """Create an instance of AStar."""
    core.add_set_locations_to_rule(AStar)
    return AStar()


@pytest.fixture
def lint_a_star(
    linter: core.Linter,
    a_star: core.BaseChecker,
) -> core.Linter:
    """Lint AStar."""
    linter.checkers.add(a_star)

    return linter


def test_a_star_rule_code(
    a_star: core.BaseChecker,
) -> None:
    """Test a_star rule code."""
    assert a_star.code == a_star.__module__.split(".")[-1]


def test_a_star_auto_fixable(
    a_star: core.BaseChecker,
) -> None:
    """Test a_star auto fixable."""
    assert a_star.is_auto_fixable is False


def test_pass_explicit_columns(
    lint_a_star: core.Linter,
) -> None:
    """Test pass in clause."""
    sql_pass: str = "SELECT city_id, logdate FROM measurement;"

    violations: core.ViolationMetric = lint_a_star.run(
        file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_count_star(
    lint_a_star: core.Linter,
) -> None:
    """Test pass in clause."""
    sql_pass: str = "SELECT count(*) FROM measurement;"

    violations: core.ViolationMetric = lint_a_star.run(
        file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_a_star(
    lint_a_star: core.Linter,
) -> None:
    """Test fail a_star."""
    sql_fail: str = "SELECT * FROM measurement;"

    violations: core.ViolationMetric = lint_a_star.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_a_star_description(
    lint_a_star: core.Linter,
    a_star: core.BaseChecker,
) -> None:
    """Test a_star description."""
    sql_fail: str = "SELECT * FROM measurement;"

    _: core.ViolationMetric = lint_a_star.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(a_star.violations),
        ).description
        == "Asterisk in column reference is discouraged"
    )


def test_pass_noqa_a_star(
    lint_a_star: core.Linter,
) -> None:
    """Test pass noqa a_star."""
    sql_pass_noqa: str = """
    -- noqa: GN029
    SELECT * FROM measurement;
    """

    violations: core.ViolationMetric = lint_a_star.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_a_star(
    lint_a_star: core.Linter,
) -> None:
    """Test fail noqa a_star."""
    sql_fail_noqa: str = """
    -- noqa: GN021
    SELECT * FROM measurement;
    """

    violations: core.ViolationMetric = lint_a_star.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_a_star(
    lint_a_star: core.Linter,
) -> None:
    """Test pass general noqa a_star."""
    sql_pass_noqa: str = """
    -- noqa:
    SELECT * FROM measurement;
    """

    violations: core.ViolationMetric = lint_a_star.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
