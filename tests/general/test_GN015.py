"""Test drop cascade."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.general.GN015 import DropCascade


@pytest.fixture(scope="module")
def drop_cascade() -> core.BaseChecker:
    """Create an instance of DropCascade."""
    core.add_apply_fix_to_rule(DropCascade)
    core.add_set_locations_to_rule(DropCascade)
    return DropCascade()


@pytest.fixture
def lint_drop_cascade(
    linter: core.Linter,
    drop_cascade: core.BaseChecker,
) -> core.Linter:
    """Lint DropCascade."""
    drop_cascade.config.lint.fix = False
    linter.checkers.add(drop_cascade)

    return linter


def test_drop_cascade_rule_code(
    drop_cascade: core.BaseChecker,
) -> None:
    """Test drop cascade rule code."""
    assert drop_cascade.code == drop_cascade.__module__.split(".")[-1]


def test_drop_cascade_auto_fixable(
    drop_cascade: core.BaseChecker,
) -> None:
    """Test drop cascade auto fixable."""
    assert drop_cascade.is_auto_fixable is True


def test_fail_drop_cascade(
    lint_drop_cascade: core.Linter,
) -> None:
    """Test fail drop cascade."""
    sql_fail: str = "DROP TABLE films_recent CASCADE;"

    violations: core.ViolationMetric = lint_drop_cascade.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_drop_cascade_description(
    lint_drop_cascade: core.Linter,
    drop_cascade: core.BaseChecker,
) -> None:
    """Test drop cascade description."""
    sql_fail: str = "DROP SCHEMA films_recent CASCADE;"

    _: core.ViolationMetric = lint_drop_cascade.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(drop_cascade.violations),
        ).description
        == "Drop cascade on `films_recent` detected"
    )


def test_pass_noqa_drop_cascade(
    lint_drop_cascade: core.Linter,
) -> None:
    """Test pass noqa drop cascade."""
    sql_pass_noqa: str = """
    -- noqa: GN015
    DROP VIEW films_recent CASCADE;
    """

    violations: core.ViolationMetric = lint_drop_cascade.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_drop_cascade(
    lint_drop_cascade: core.Linter,
) -> None:
    """Test fail noqa drop cascade."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE films_recent DROP CONSTRAINT films_recent_pkey CASCADE;
    """

    violations: core.ViolationMetric = lint_drop_cascade.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_drop_cascade(
    lint_drop_cascade: core.Linter,
) -> None:
    """Test fail noqa drop cascade."""
    sql_pass_noqa: str = """
    -- noqa:
    ALTER TABLE films_recent DROP COLUMN id CASCADE;
    """

    violations: core.ViolationMetric = lint_drop_cascade.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_drop_cascade(
    lint_drop_cascade: core.Linter,
    drop_cascade: core.BaseChecker,
) -> None:
    """Test fail fix drop cascade."""
    sql_fail: str = "DROP MATERIALIZED VIEW films_recent CASCADE;"

    sql_fix: str = "DROP MATERIALIZED VIEW films_recent;"

    drop_cascade.config.lint.fix = True

    violations: core.ViolationMetric = lint_drop_cascade.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_drop_cascade(
    lint_drop_cascade: core.Linter,
    drop_cascade: core.BaseChecker,
) -> None:
    """Test fail fix drop cascade."""
    sql_fail: str = "ALTER TABLE films_recent DROP COLUMN films_recent CASCADE;"

    sql_fix: str = "ALTER TABLE films_recent\n    DROP COLUMN films_recent;"

    drop_cascade.config.lint.fix = True

    violations: core.ViolationMetric = lint_drop_cascade.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
