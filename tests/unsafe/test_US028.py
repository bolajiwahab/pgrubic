"""Test non concurrent refresh materialized view."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US028 import NonConcurrentRefreshMaterializedView


@pytest.fixture(scope="module")
def non_concurrent_refresh_materialized_view() -> core.BaseChecker:
    """Create an instance of NonConcurrentRefreshMaterializedView."""
    core.add_apply_fix_to_rule(NonConcurrentRefreshMaterializedView)
    core.add_set_locations_to_rule(NonConcurrentRefreshMaterializedView)
    return NonConcurrentRefreshMaterializedView()


@pytest.fixture
def lint_non_concurrent_refresh_materialized_view(
    linter: core.Linter,
    non_concurrent_refresh_materialized_view: core.BaseChecker,
) -> core.Linter:
    """Lint NonConcurrentRefreshMaterializedView."""
    non_concurrent_refresh_materialized_view.config.lint.fix = False
    linter.checkers.add(non_concurrent_refresh_materialized_view)

    return linter


def test_non_concurrent_refresh_materialized_view_rule_code(
    non_concurrent_refresh_materialized_view: core.BaseChecker,
) -> None:
    """Test non concurrent refresh materialized view rule code."""
    assert (
        non_concurrent_refresh_materialized_view.code
        == non_concurrent_refresh_materialized_view.__module__.split(
            ".",
        )[-1]
    )


def test_non_concurrent_refresh_materialized_view_auto_fixable(
    non_concurrent_refresh_materialized_view: core.BaseChecker,
) -> None:
    """Test non concurrent refresh materialized view auto fixable."""
    assert non_concurrent_refresh_materialized_view.is_auto_fixable is True


def test_pass_concurrent_detach_partition(
    lint_non_concurrent_refresh_materialized_view: core.Linter,
) -> None:
    """Test pass concurrent refresh materialized view."""
    sql_pass: str = "REFRESH MATERIALIZED VIEW CONCURRENTLY tbl;"

    violations: core.ViolationMetric = lint_non_concurrent_refresh_materialized_view.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_refresh_materialized_view(
    lint_non_concurrent_refresh_materialized_view: core.Linter,
) -> None:
    """Test non concurrent refresh materialized view."""
    sql_fail: str = "REFRESH MATERIALIZED VIEW tbl;"

    violations: core.ViolationMetric = lint_non_concurrent_refresh_materialized_view.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_refresh_materialized_view_description(
    lint_non_concurrent_refresh_materialized_view: core.Linter,
    non_concurrent_refresh_materialized_view: core.BaseChecker,
) -> None:
    """Test non concurrent refresh materialized view description."""
    sql_fail: str = "REFRESH MATERIALIZED VIEW tbl;"

    _: core.ViolationMetric = lint_non_concurrent_refresh_materialized_view.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(non_concurrent_refresh_materialized_view.violations),
        ).description
        == "Non concurrent refresh materialized view"
    )


def test_pass_noqa_non_concurrent_refresh_materialized_view(
    lint_non_concurrent_refresh_materialized_view: core.Linter,
) -> None:
    """Test pass noqa non concurrent refresh materialized view."""
    sql_pass_noqa: str = """
    -- noqa: US028
    REFRESH MATERIALIZED VIEW tbl;
    """

    violations: core.ViolationMetric = lint_non_concurrent_refresh_materialized_view.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_non_concurrent_refresh_materialized_view(
    lint_non_concurrent_refresh_materialized_view: core.Linter,
) -> None:
    """Test fail noqa non concurrent refresh materialized view."""
    sql_noqa: str = """
    -- noqa: US001
    REFRESH MATERIALIZED VIEW tbl;
    """

    violations: core.ViolationMetric = lint_non_concurrent_refresh_materialized_view.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_non_concurrent_refresh_materialized_view(
    lint_non_concurrent_refresh_materialized_view: core.Linter,
) -> None:
    """Test pass noqa non concurrent refresh materialized view."""
    sql_noqa: str = """
    -- noqa
    REFRESH MATERIALIZED VIEW tbl;
    """

    violations: core.ViolationMetric = lint_non_concurrent_refresh_materialized_view.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_non_concurrent_refresh_materialized_view(
    lint_non_concurrent_refresh_materialized_view: core.Linter,
    non_concurrent_refresh_materialized_view: core.BaseChecker,
) -> None:
    """Test fail fix non concurrent refresh materialized view."""
    sql_fail: str = "REFRESH MATERIALIZED VIEW tbl;"

    sql_fix: str = "REFRESH MATERIALIZED VIEW CONCURRENTLY tbl;\n"

    non_concurrent_refresh_materialized_view.config.lint.fix = True

    violations: core.ViolationMetric = lint_non_concurrent_refresh_materialized_view.run(
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
