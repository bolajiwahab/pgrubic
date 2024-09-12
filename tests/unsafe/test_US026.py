"""Test vacuum full."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.US026 import VacuumFull


@pytest.fixture(scope="module")
def vacuum_full() -> core.BaseChecker:
    """Create an instance of VacuumFull."""
    core.add_set_locations_to_rule(VacuumFull)
    return VacuumFull()


@pytest.fixture
def lint_cluster(
    linter: core.Linter,
    vacuum_full: core.BaseChecker,
) -> core.Linter:
    """Lint VacuumFull."""
    linter.checkers.add(vacuum_full)

    return linter


def test_cluster_rule_code(
    vacuum_full: core.BaseChecker,
) -> None:
    """Test vacuum full rule code."""
    assert (
        vacuum_full.code
        == vacuum_full.__module__.split(
            ".",
        )[-1]
    )


def test_cluster_auto_fixable(
    vacuum_full: core.BaseChecker,
) -> None:
    """Test vacuum full auto fixable."""
    assert vacuum_full.is_auto_fixable is False


def test_fail_cluster(
    lint_cluster: core.Linter,
) -> None:
    """Test vacuum full."""
    sql_fail: str = "VACUUM FULL employees;"

    violations: core.ViolationMetric = lint_cluster.run(
        source_path=SOURCE_PATH,
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
    vacuum_full: core.BaseChecker,
) -> None:
    """Test vacuum full description."""
    sql_fail: str = "VACUUM FULL employees;"

    _: core.ViolationMetric = lint_cluster.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(vacuum_full.violations),
        ).description
        == "Vacuum full found"
    )


def test_pass_noqa_cluster(
    lint_cluster: core.Linter,
) -> None:
    """Test pass noqa vacuum full."""
    sql_pass_noqa: str = """
    -- noqa: US026
    VACUUM FULL employees;
    """

    violations: core.ViolationMetric = lint_cluster.run(
        source_path=SOURCE_PATH,
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
    """Test fail noqa vacuum full."""
    sql_noqa: str = """
    -- noqa: US001
    VACUUM FULL employees;
    """

    violations: core.ViolationMetric = lint_cluster.run(
        source_path=SOURCE_PATH,
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
    """Test pass noqa vacuum full."""
    sql_noqa: str = """
    -- noqa:
    VACUUM FULL employees;
    """

    violations: core.ViolationMetric = lint_cluster.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
