"""Test multi column partitioning."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN018 import MultiColumnPartitioning


@pytest.fixture(scope="module")
def multi_column_partitioning() -> core.BaseChecker:
    """Create an instance of MultiColumnPartitioning."""
    core.add_set_locations_to_rule(MultiColumnPartitioning)
    return MultiColumnPartitioning()


@pytest.fixture
def lint_multi_column_partitioning(
    linter: core.Linter,
    multi_column_partitioning: core.BaseChecker,
) -> core.Linter:
    """Lint MultiColumnPartitioning."""
    linter.checkers.add(multi_column_partitioning)

    return linter


def test_multi_column_partitioning_rule_code(
    multi_column_partitioning: core.BaseChecker,
) -> None:
    """Test multi column partitioning rule code."""
    assert (
        multi_column_partitioning.code
        == multi_column_partitioning.__module__.split(".")[-1]
    )


def test_multi_column_partitioning_auto_fixable(
    multi_column_partitioning: core.BaseChecker,
) -> None:
    """Test multi column partitioning auto fixable."""
    assert multi_column_partitioning.is_auto_fixable is False


def test_pass_single_column_partitioning(
    lint_multi_column_partitioning: core.Linter,
) -> None:
    """Test pass multi column partitioning."""
    sql_pass: str = """
    CREATE TABLE measurement (
        city_id int not null,
        logdate date not null
    ) PARTITION BY RANGE (logdate);
    """

    violations: core.ViolationMetric = lint_multi_column_partitioning.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_multi_column_partitioning(
    lint_multi_column_partitioning: core.Linter,
) -> None:
    """Test fail multi column partitioning."""
    sql_fail: str = """
    CREATE TABLE measurement (
        city_id int not null,
        logdate date not null
    ) PARTITION BY RANGE (city_id, logdate);
    """

    violations: core.ViolationMetric = lint_multi_column_partitioning.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_multi_column_partitioning_description(
    lint_multi_column_partitioning: core.Linter,
    multi_column_partitioning: core.BaseChecker,
) -> None:
    """Test multi column partitioning description."""
    sql_fail: str = """
    CREATE TABLE measurement (
        city_id int not null,
        logdate date not null
    ) PARTITION BY RANGE (city_id, logdate);
    """

    _: core.ViolationMetric = lint_multi_column_partitioning.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(multi_column_partitioning.violations),
        ).description
        == "Prefer partitioning by one key"
    )


def test_pass_noqa_multi_column_partitioning(
    lint_multi_column_partitioning: core.Linter,
) -> None:
    """Test pass noqa multi column partitioning."""
    sql_pass_noqa: str = """
    -- noqa: GN018
    CREATE TABLE measurement (
        city_id int not null,
        logdate date not null
    ) PARTITION BY RANGE (city_id, logdate);
    """

    violations: core.ViolationMetric = lint_multi_column_partitioning.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_multi_column_partitioning(
    lint_multi_column_partitioning: core.Linter,
) -> None:
    """Test fail noqa multi column partitioning."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE measurement (
        city_id int not null,
        logdate date not null
    ) PARTITION BY RANGE (city_id, logdate);
    """

    violations: core.ViolationMetric = lint_multi_column_partitioning.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_multi_column_partitioning(
    lint_multi_column_partitioning: core.Linter,
) -> None:
    """Test fail noqa multi column partitioning."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE measurement (
        city_id int not null,
        logdate date not null
    ) PARTITION BY RANGE (city_id, logdate);
    """

    violations: core.ViolationMetric = lint_multi_column_partitioning.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
