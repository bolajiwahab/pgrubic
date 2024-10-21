"""Test non concurrent index drop."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US019 import NonConcurrentIndexDrop


@pytest.fixture(scope="module")
def non_concurrent_index_drop() -> core.BaseChecker:
    """Create an instance of NonConcurrentIndexDrop."""
    core.add_apply_fix_to_rule(NonConcurrentIndexDrop)
    core.add_set_locations_to_rule(NonConcurrentIndexDrop)
    return NonConcurrentIndexDrop()


@pytest.fixture
def lint_non_concurrent_index_drop(
    linter: core.Linter,
    non_concurrent_index_drop: core.BaseChecker,
) -> core.Linter:
    """Lint NonConcurrentIndexDrop."""
    non_concurrent_index_drop.config.lint.fix = False
    linter.checkers.add(non_concurrent_index_drop)

    return linter


def test_non_concurrent_index_drop_rule_code(
    non_concurrent_index_drop: core.BaseChecker,
) -> None:
    """Test non concurrent index drop rule code."""
    assert (
        non_concurrent_index_drop.code
        == non_concurrent_index_drop.__module__.split(
            ".",
        )[-1]
    )


def test_non_concurrent_index_drop_auto_fixable(
    non_concurrent_index_drop: core.BaseChecker,
) -> None:
    """Test non concurrent index drop auto fixable."""
    assert non_concurrent_index_drop.is_auto_fixable is True


def test_pass_concurrent_index_creation(
    lint_non_concurrent_index_drop: core.Linter,
) -> None:
    """Test pass concurrent index creation."""
    sql_pass: str = "DROP INDEX CONCURRENTLY idx;"

    violations: core.ViolationMetric = lint_non_concurrent_index_drop.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_index_drop(
    lint_non_concurrent_index_drop: core.Linter,
) -> None:
    """Test non concurrent index drop."""
    sql_fail: str = "DROP INDEX idx;"

    violations: core.ViolationMetric = lint_non_concurrent_index_drop.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_index_drop_description(
    lint_non_concurrent_index_drop: core.Linter,
    non_concurrent_index_drop: core.BaseChecker,
) -> None:
    """Test non concurrent index drop description."""
    sql_fail: str = "DROP INDEX idx;"

    _: core.ViolationMetric = lint_non_concurrent_index_drop.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(non_concurrent_index_drop.violations),
        ).description
        == "Non concurrent index drop"
    )


def test_pass_noqa_non_concurrent_index_drop(
    lint_non_concurrent_index_drop: core.Linter,
) -> None:
    """Test pass noqa non concurrent index drop."""
    sql_pass_noqa: str = """
    -- noqa: US019
    DROP INDEX idx;
    """

    violations: core.ViolationMetric = lint_non_concurrent_index_drop.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_non_concurrent_index_drop(
    lint_non_concurrent_index_drop: core.Linter,
) -> None:
    """Test fail noqa non concurrent index drop."""
    sql_noqa: str = """
    -- noqa: US001
    DROP INDEX idx;
    """

    violations: core.ViolationMetric = lint_non_concurrent_index_drop.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_non_concurrent_index_drop(
    lint_non_concurrent_index_drop: core.Linter,
) -> None:
    """Test pass noqa non concurrent index drop."""
    sql_noqa: str = """
    -- noqa
    DROP INDEX idx;
    """

    violations: core.ViolationMetric = lint_non_concurrent_index_drop.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_non_concurrent_index_drop(
    lint_non_concurrent_index_drop: core.Linter,
    non_concurrent_index_drop: core.BaseChecker,
) -> None:
    """Test fail fix non concurrent index drop."""
    sql_fail: str = "DROP INDEX idx;"

    sql_fix: str = "DROP INDEX CONCURRENTLY idx;"

    non_concurrent_index_drop.config.lint.fix = True

    violations: core.ViolationMetric = lint_non_concurrent_index_drop.run(
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
