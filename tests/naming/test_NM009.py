"""Test invalid partition name."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.naming.NM009 import InvalidPartitionName


@pytest.fixture(scope="module")
def invalid_partition_name() -> core.BaseChecker:
    """Create an instance of invalid partition name."""
    core.add_set_locations_to_rule(InvalidPartitionName)
    return InvalidPartitionName()


@pytest.fixture
def lint_invalid_partition_name(
    linter: core.Linter,
    invalid_partition_name: core.BaseChecker,
) -> core.Linter:
    """Lint invalid partition name."""
    invalid_partition_name.config.lint.regex_partition = (
        "[a-zA-Z0-9]+__[a-zA-Z0-9_]+__[a-zA-Z0-9_]+$"
    )

    linter.checkers.add(invalid_partition_name)

    return linter


def test_invalid_partition_name_rule_code(
    invalid_partition_name: core.BaseChecker,
) -> None:
    """Test invalid partition name rule code."""
    assert invalid_partition_name.code == invalid_partition_name.__module__.split(".")[-1]


def test_invalid_partition_name_auto_fixable(
    invalid_partition_name: core.BaseChecker,
) -> None:
    """Test invalid partition name auto fixable."""
    assert invalid_partition_name.is_auto_fixable is False


def test_pass_valid_partition_name(
    lint_invalid_partition_name: core.Linter,
) -> None:
    """Test pass implicit invalid partition name."""
    sql_pass: str = """
    CREATE TABLE public__measurement__2024_02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');
    """

    violations: core.ViolationMetric = lint_invalid_partition_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_invalid_partition_name(
    lint_invalid_partition_name: core.Linter,
) -> None:
    """Test fail invalid partition name."""
    sql_fail: str = """
    CREATE TABLE measurement__2024_02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');
    """

    violations: core.ViolationMetric = lint_invalid_partition_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_invalid_partition_name_description(
    lint_invalid_partition_name: core.Linter,
    invalid_partition_name: core.BaseChecker,
) -> None:
    """Test invalid partition name description."""
    sql_fail: str = """
    CREATE TABLE measurement__2024_02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');
    """

    _: core.ViolationMetric = lint_invalid_partition_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(invalid_partition_name.violations),
        ).description
        == f"Partition `measurement__2024_02` does not follow naming convention `{invalid_partition_name.config.lint.regex_partition}`"  # noqa: E501
    )


def test_pass_noqa_invalid_partition_name(
    lint_invalid_partition_name: core.Linter,
) -> None:
    """Test pass noqa invalid partition name."""
    sql_pass_noqa: str = """
    -- noqa: NM009
    CREATE TABLE measurement__2024_02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');
    """

    violations: core.ViolationMetric = lint_invalid_partition_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_invalid_partition_name(
    lint_invalid_partition_name: core.Linter,
) -> None:
    """Test fail noqa invalid partition name."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE measurement__2024_02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');
    """

    violations: core.ViolationMetric = lint_invalid_partition_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_invalid_partition_name(
    lint_invalid_partition_name: core.Linter,
) -> None:
    """Test pass noqa invalid partition name."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE measurement__2024_02 PARTITION OF measurement
    FOR VALUES FROM ('2006-02-01') TO ('2006-03-01');
    """

    violations: core.ViolationMetric = lint_invalid_partition_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
