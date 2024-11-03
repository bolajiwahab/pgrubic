"""Test null constraint."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN024 import NullComparison


@pytest.fixture(scope="module")
def null_comparison() -> core.BaseChecker:
    """Create an instance of NullComparison."""
    core.add_apply_fix_to_rule(NullComparison)
    core.add_set_locations_to_rule(NullComparison)
    return NullComparison()


@pytest.fixture
def lint_null_comparison(
    linter: core.Linter,
    null_comparison: core.BaseChecker,
) -> core.Linter:
    """Lint NullComparison."""
    null_comparison.config.lint.fix = False
    linter.checkers.add(null_comparison)

    return linter


def test_null_comparison_rule_code(
    null_comparison: core.BaseChecker,
) -> None:
    """Test null constraint rule code."""
    assert null_comparison.code == null_comparison.__module__.split(".")[-1]


def test_null_comparison_auto_fixable(
    null_comparison: core.BaseChecker,
) -> None:
    """Test null constraint auto fixable."""
    assert null_comparison.is_auto_fixable is True


def test_pass_null_comparisonstamp(
    lint_null_comparison: core.Linter,
) -> None:
    """Test pass null constraint."""
    sql_pass: str = "SELECT a IS NULL;"

    violations: core.ViolationMetric = lint_null_comparison.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_null_comparison(
    lint_null_comparison: core.Linter,
) -> None:
    """Test fail null constraint."""
    sql_fail: str = "SELECT a = NULL;"

    violations: core.ViolationMetric = lint_null_comparison.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_null_comparison_description(
    lint_null_comparison: core.Linter,
    null_comparison: core.BaseChecker,
) -> None:
    """Test null constraint description."""
    sql_fail: str = "SELECT a != NULL;"

    _: core.ViolationMetric = lint_null_comparison.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(null_comparison.violations),
        ).description
        == "Comparison with NULL should be [IS | IS NOT] NULL"
    )


def test_pass_noqa_null_comparison(
    lint_null_comparison: core.Linter,
) -> None:
    """Test pass noqa null constraint."""
    sql_pass_noqa: str = """
    -- noqa: GN024
    SELECT NULL <> a;
    """

    violations: core.ViolationMetric = lint_null_comparison.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_null_comparison(
    lint_null_comparison: core.Linter,
) -> None:
    """Test fail noqa null constraint."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    SELECT NULL = NULL;
    """

    violations: core.ViolationMetric = lint_null_comparison.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_null_comparison(
    lint_null_comparison: core.Linter,
) -> None:
    """Test fail noqa null constraint."""
    sql_pass_noqa: str = """
    -- noqa
    SELECT a = NULL;
    """

    violations: core.ViolationMetric = lint_null_comparison.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_is_null_null_comparison(
    lint_null_comparison: core.Linter,
    null_comparison: core.BaseChecker,
) -> None:
    """Test fail fix null constraint."""
    sql_fail: str = "SELECT a = NULL;"

    sql_fix: str = "SELECT a IS NULL;\n"

    null_comparison.config.lint.fix = True

    violations: core.ViolationMetric = lint_null_comparison.run(
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


def test_fail_fix_is_not_null_null_comparison(
    lint_null_comparison: core.Linter,
    null_comparison: core.BaseChecker,
) -> None:
    """Test fail fix null constraint."""
    sql_fail: str = "SELECT NULL != a;"

    sql_fix: str = "SELECT a IS NOT NULL;\n"

    null_comparison.config.lint.fix = True

    violations: core.ViolationMetric = lint_null_comparison.run(
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
