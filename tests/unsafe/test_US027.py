"""Test non concurrent detach partition."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US027 import NonConcurrentDetachPartition


@pytest.fixture(scope="module")
def non_concurrent_detach_partition() -> core.BaseChecker:
    """Create an instance of NonConcurrentDetachPartition."""
    core.add_apply_fix_to_rule(NonConcurrentDetachPartition)
    core.add_set_locations_to_rule(NonConcurrentDetachPartition)
    return NonConcurrentDetachPartition()


@pytest.fixture
def lint_non_concurrent_detach_partition(
    linter: core.Linter,
    non_concurrent_detach_partition: core.BaseChecker,
) -> core.Linter:
    """Lint NonConcurrentDetachPartition."""
    non_concurrent_detach_partition.config.lint.fix = False
    linter.checkers.add(non_concurrent_detach_partition)

    return linter


def test_non_concurrent_detach_partition_rule_code(
    non_concurrent_detach_partition: core.BaseChecker,
) -> None:
    """Test non concurrent detach partition rule code."""
    assert (
        non_concurrent_detach_partition.code
        == non_concurrent_detach_partition.__module__.split(
            ".",
        )[-1]
    )


def test_non_concurrent_detach_partition_auto_fixable(
    non_concurrent_detach_partition: core.BaseChecker,
) -> None:
    """Test non concurrent detach partition auto fixable."""
    assert non_concurrent_detach_partition.is_auto_fixable is True


def test_pass_concurrent_detach_partition(
    lint_non_concurrent_detach_partition: core.Linter,
) -> None:
    """Test pass concurrent detach partition."""
    sql_pass: str = "ALTER TABLE tbl DETACH PARTITION tbl_y2006m02 CONCURRENTLY;"

    violations: core.ViolationMetric = lint_non_concurrent_detach_partition.run(
        file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_detach_partition(
    lint_non_concurrent_detach_partition: core.Linter,
) -> None:
    """Test non concurrent detach partition."""
    sql_fail: str = "ALTER TABLE tbl DETACH PARTITION tbl_y2006m02;"

    violations: core.ViolationMetric = lint_non_concurrent_detach_partition.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_detach_partition_description(
    lint_non_concurrent_detach_partition: core.Linter,
    non_concurrent_detach_partition: core.BaseChecker,
) -> None:
    """Test non concurrent detach partition description."""
    sql_fail: str = "ALTER TABLE tbl DETACH PARTITION tbl_y2006m02;"

    _: core.ViolationMetric = lint_non_concurrent_detach_partition.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(non_concurrent_detach_partition.violations),
        ).description
        == "Non concurrent detach partition"
    )


def test_pass_noqa_non_concurrent_detach_partition(
    lint_non_concurrent_detach_partition: core.Linter,
) -> None:
    """Test pass noqa non concurrent detach partition."""
    sql_pass_noqa: str = """
    -- noqa: US027
    ALTER TABLE tbl DETACH PARTITION tbl_y2006m02;
    """

    violations: core.ViolationMetric = lint_non_concurrent_detach_partition.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_non_concurrent_detach_partition(
    lint_non_concurrent_detach_partition: core.Linter,
) -> None:
    """Test fail noqa non concurrent detach partition."""
    sql_noqa: str = """
    -- noqa: US001
    ALTER TABLE tbl DETACH PARTITION tbl_y2006m02;
    """

    violations: core.ViolationMetric = lint_non_concurrent_detach_partition.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_non_concurrent_detach_partition(
    lint_non_concurrent_detach_partition: core.Linter,
) -> None:
    """Test pass noqa non concurrent detach partition."""
    sql_noqa: str = """
    -- noqa:
    ALTER TABLE tbl DETACH PARTITION tbl_y2006m02;
    """

    violations: core.ViolationMetric = lint_non_concurrent_detach_partition.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_non_concurrent_detach_partition(
    lint_non_concurrent_detach_partition: core.Linter,
    non_concurrent_detach_partition: core.BaseChecker,
) -> None:
    """Test fail fix non concurrent detach partition."""
    sql_fail: str = "ALTER TABLE tbl DETACH PARTITION tbl_y2006m02;"

    sql_fix: str = "ALTER TABLE tbl\n    DETACH PARTITION tbl_y2006m02 CONCURRENTLY;"

    non_concurrent_detach_partition.config.lint.fix = True

    violations: core.ViolationMetric = lint_non_concurrent_detach_partition.run(
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
