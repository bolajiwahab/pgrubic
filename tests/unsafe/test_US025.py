"""Test cluster."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US025 import Cluster


@pytest.fixture(scope="module")
def cluster() -> core.BaseChecker:
    """Create an instance of Cluster."""
    core.add_set_locations_to_rule(Cluster)
    return Cluster()


@pytest.fixture
def lint_cluster(
    linter: core.Linter,
    cluster: core.BaseChecker,
) -> core.Linter:
    """Lint Cluster."""
    linter.checkers.add(cluster)

    return linter


def test_cluster_rule_code(
    cluster: core.BaseChecker,
) -> None:
    """Test cluster rule code."""
    assert (
        cluster.code
        == cluster.__module__.split(
            ".",
        )[-1]
    )


def test_cluster_auto_fixable(
    cluster: core.BaseChecker,
) -> None:
    """Test cluster auto fixable."""
    assert cluster.is_auto_fixable is False


def test_fail_cluster(
    lint_cluster: core.Linter,
) -> None:
    """Test cluster."""
    sql_fail: str = "CLUSTER employees USING employees_ind;"

    violations: core.ViolationMetric = lint_cluster.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_cluster_description(
    lint_cluster: core.Linter,
    cluster: core.BaseChecker,
) -> None:
    """Test cluster description."""
    sql_fail: str = "CLUSTER employees;"

    _: core.ViolationMetric = lint_cluster.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(cluster.violations),
        ).description
        == "Cluster found"
    )


def test_pass_noqa_cluster(
    lint_cluster: core.Linter,
) -> None:
    """Test pass noqa cluster."""
    sql_pass_noqa: str = """
    -- noqa: US025
    CLUSTER employees;
    """

    violations: core.ViolationMetric = lint_cluster.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_cluster(
    lint_cluster: core.Linter,
) -> None:
    """Test fail noqa cluster."""
    sql_noqa: str = """
    -- noqa: US001
    CLUSTER;
    """

    violations: core.ViolationMetric = lint_cluster.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_cluster(
    lint_cluster: core.Linter,
) -> None:
    """Test pass noqa cluster."""
    sql_noqa: str = """
    -- noqa
    CLUSTER employees USING employees_ind;
    """

    violations: core.ViolationMetric = lint_cluster.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
