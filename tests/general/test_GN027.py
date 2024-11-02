"""Test yoda condition."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN027 import YodaCondition


@pytest.fixture(scope="module")
def yoda_condition() -> core.BaseChecker:
    """Create an instance of YodaCondition."""
    core.add_apply_fix_to_rule(YodaCondition)
    core.add_set_locations_to_rule(YodaCondition)
    return YodaCondition()


@pytest.fixture
def lint_yoda_condition(
    linter: core.Linter,
    yoda_condition: core.BaseChecker,
) -> core.Linter:
    """Lint YodaCondition."""
    yoda_condition.config.lint.fix = False
    linter.checkers.add(yoda_condition)

    return linter


def test_yoda_condition_rule_code(
    yoda_condition: core.BaseChecker,
) -> None:
    """Test yoda condition rule code."""
    assert yoda_condition.code == yoda_condition.__module__.split(".")[-1]


def test_yoda_condition_auto_fixable(
    yoda_condition: core.BaseChecker,
) -> None:
    """Test yoda condition auto fixable."""
    assert yoda_condition.is_auto_fixable is True


def test_pass_non_yoda_condition(
    lint_yoda_condition: core.Linter,
) -> None:
    """Test pass non yoda condition."""
    sql_pass: str = "SELECT * FROM measurement WHERE city_id = 10;"

    violations: core.ViolationMetric = lint_yoda_condition.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_non_yoda_condition_constant_on_left_and_right(
    lint_yoda_condition: core.Linter,
) -> None:
    """Test pass non yoda condition."""
    sql_pass: str = "SELECT * FROM measurement WHERE 10 = 10;"

    violations: core.ViolationMetric = lint_yoda_condition.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_yoda_condition(
    lint_yoda_condition: core.Linter,
) -> None:
    """Test fail yoda condition."""
    sql_fail: str = "SELECT * FROM measurement WHERE 10 = city_id;"

    violations: core.ViolationMetric = lint_yoda_condition.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_yoda_condition_description(
    lint_yoda_condition: core.Linter,
    yoda_condition: core.BaseChecker,
) -> None:
    """Test yoda condition description."""
    sql_fail: str = "SELECT * FROM measurement WHERE 10 = city_id;"

    _: core.ViolationMetric = lint_yoda_condition.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(yoda_condition.violations),
        ).description
        == "Yoda conditions are discouraged"
    )


def test_pass_noqa_yoda_condition(
    lint_yoda_condition: core.Linter,
) -> None:
    """Test pass noqa yoda condition."""
    sql_pass_noqa: str = """
    -- noqa: GN027
    SELECT * FROM measurement WHERE 10 = city_id;
    """

    violations: core.ViolationMetric = lint_yoda_condition.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_yoda_condition(
    lint_yoda_condition: core.Linter,
) -> None:
    """Test fail noqa yoda condition."""
    sql_fail_noqa: str = """
    -- noqa: GN021
    SELECT * FROM measurement WHERE 10 = city_id;
    """

    violations: core.ViolationMetric = lint_yoda_condition.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_yoda_condition(
    lint_yoda_condition: core.Linter,
) -> None:
    """Test pass general noqa yoda condition."""
    sql_pass_noqa: str = """
    -- noqa
    SELECT * FROM measurement WHERE 10 = city_id;
    """

    violations: core.ViolationMetric = lint_yoda_condition.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_yoda_condition(
    lint_yoda_condition: core.Linter,
    yoda_condition: core.BaseChecker,
) -> None:
    """Test fail fix yoda condition."""
    sql_fail: str = "SELECT * FROM measurement WHERE 10 = city_id;"

    sql_fix: str = "SELECT *\n  FROM measurement\n WHERE city_id = 10;\n"

    yoda_condition.config.lint.fix = True

    violations: core.ViolationMetric = lint_yoda_condition.run(
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
