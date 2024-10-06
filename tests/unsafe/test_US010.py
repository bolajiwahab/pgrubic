"""Test not null constraint on existing on existing column."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.US010 import NotNullConstraintOnExistingColumn


@pytest.fixture(scope="module")
def not_null_constraint_on_existing_column() -> core.BaseChecker:
    """Create an instance of NotNullConstraintOnExistingColumn."""
    core.add_set_locations_to_rule(NotNullConstraintOnExistingColumn)
    return NotNullConstraintOnExistingColumn()


@pytest.fixture
def lint_not_null_constraint_on_existing_column(
    linter: core.Linter,
    not_null_constraint_on_existing_column: core.BaseChecker,
) -> core.Linter:
    """Lint NotNullConstraintOnExistingColumn."""
    linter.checkers.add(not_null_constraint_on_existing_column)

    return linter


def test_not_null_constraint_on_existing_column_rule_code(
    not_null_constraint_on_existing_column: core.BaseChecker,
) -> None:
    """Test not null constraint on existing column rule code."""
    assert (
        not_null_constraint_on_existing_column.code
        == not_null_constraint_on_existing_column.__module__.split(".")[-1]
    )


def test_not_null_constraint_on_existing_column_auto_fixable(
    not_null_constraint_on_existing_column: core.BaseChecker,
) -> None:
    """Test not null constraint on existing column auto fixable."""
    assert not_null_constraint_on_existing_column.is_auto_fixable is False


def test_fail_not_null_constraint_on_existing_column(
    lint_not_null_constraint_on_existing_column: core.Linter,
) -> None:
    """Test fail not null constraint on existing column."""
    sql_fail: str = """
    ALTER TABLE public.card ALTER COLUMN id SET NOT NULL
    ;
    """

    violations: core.ViolationMetric = lint_not_null_constraint_on_existing_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_not_null_constraint_on_existing_column_description(
    lint_not_null_constraint_on_existing_column: core.Linter,
    not_null_constraint_on_existing_column: core.BaseChecker,
) -> None:
    """Test fail not null constraint on existing column description."""
    sql_fail: str = """
    ALTER TABLE public.card ALTER COLUMN id SET NOT NULL
    ;
    """

    _: core.ViolationMetric = lint_not_null_constraint_on_existing_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(iter(not_null_constraint_on_existing_column.violations)).description
        == "Not null constraint on existing column `id`"
    )


def test_pass_noqa_not_null_constraint_on_existing_column(
    lint_not_null_constraint_on_existing_column: core.Linter,
) -> None:
    """Test pass noqa not null constraint on existing column."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card ALTER COLUMN id SET NOT NULL -- noqa: US010
    ;
    """

    violations: core.ViolationMetric = lint_not_null_constraint_on_existing_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_not_null_constraint_on_existing_column(
    lint_not_null_constraint_on_existing_column: core.Linter,
) -> None:
    """Test fail noqa not null constraint on existing column."""
    sql_noqa: str = """
    ALTER TABLE public.card ALTER COLUMN id SET NOT NULL -- noqa: US002
    ;
    """

    violations: core.ViolationMetric = lint_not_null_constraint_on_existing_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_not_null_constraint_on_existing_column(
    lint_not_null_constraint_on_existing_column: core.Linter,
) -> None:
    """Test fail noqa not null constraint on existing column."""
    sql_noqa: str = """
    ALTER TABLE public.card ALTER COLUMN id SET NOT NULL -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_not_null_constraint_on_existing_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
