"""Test not null constraint on new column with no static default."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.UN011 import NotNullConstraintOnNewColumnWithNoStaticDefault


@pytest.fixture(scope="module")
def not_null_constraint_on_new_column_with_no_static_default() -> core.BaseChecker:
    """Create an instance of NotNullConstraintOnNewColumnWithNoStaticDefault."""
    return NotNullConstraintOnNewColumnWithNoStaticDefault()


@pytest.fixture
def lint_not_null_constraint_on_new_column_with_no_static_default(
    linter: core.Linter,
    not_null_constraint_on_new_column_with_no_static_default: core.BaseChecker,
) -> core.Linter:
    """Lint NotNullConstraintOnNewColumnWithNoStaticDefault."""
    linter.checkers.add(not_null_constraint_on_new_column_with_no_static_default)

    return linter


def test_not_null_constraint_on_new_column_with_no_static_default_rule_code(
    not_null_constraint_on_new_column_with_no_static_default: core.BaseChecker,
) -> None:
    """Test not null constraint on new column with no static default rule code."""
    assert (
        not_null_constraint_on_new_column_with_no_static_default.code
        == not_null_constraint_on_new_column_with_no_static_default.__module__.split(
            ".",
        )[-1]
    )


def test_not_null_constraint_on_new_column_with_no_static_default_auto_fixable(
    not_null_constraint_on_new_column_with_no_static_default: core.BaseChecker,
) -> None:
    """Test not null constraint on new column with no static default auto fixable."""
    assert (
        not_null_constraint_on_new_column_with_no_static_default.is_auto_fixable
        is False
    )


def test_pass_not_null_constraint_on_new_column_with_no_static_default(
    lint_not_null_constraint_on_new_column_with_no_static_default: core.Linter,
) -> None:
    """Test not null constraint on new column with no static default."""
    sql_pass: str = """
    ALTER TABLE public.card ADD COLUMN id bigint NOT NULL DEFAULT 0
    ;
    """

    violations: core.ViolationMetric = (
        lint_not_null_constraint_on_new_column_with_no_static_default.run(
            source_path=SOURCE_PATH,
            source_code=sql_pass,
        )
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_not_null_constraint_on_new_column_with_no_static_default(
    lint_not_null_constraint_on_new_column_with_no_static_default: core.Linter,
) -> None:
    """Test not null constraint on new column with no static default."""
    sql_fail: str = """
    ALTER TABLE public.card ADD COLUMN id bigint NOT NULL
    ;
    """

    violations: core.ViolationMetric = (
        lint_not_null_constraint_on_new_column_with_no_static_default.run(
            source_path=SOURCE_PATH,
            source_code=sql_fail,
        )
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_not_null_constraint_on_new_column_with_no_static_default_description(
    lint_not_null_constraint_on_new_column_with_no_static_default: core.Linter,
    not_null_constraint_on_new_column_with_no_static_default: core.BaseChecker,
) -> None:
    """Test not null constraint on new column with no static default description."""
    sql_fail: str = """
    ALTER TABLE public.card ADD COLUMN id bigint NOT NULL
    ;
    """

    _: core.ViolationMetric = (
        lint_not_null_constraint_on_new_column_with_no_static_default.run(
            source_path=SOURCE_PATH,
            source_code=sql_fail,
        )
    )

    assert (
        next(
            iter(not_null_constraint_on_new_column_with_no_static_default.violations),
        ).description
        == "Not null constraint on new column with no static default"
    )


def test_pass_noqa_not_null_constraint_on_new_column_with_no_static_default(
    lint_not_null_constraint_on_new_column_with_no_static_default: core.Linter,
) -> None:
    """Test pass noqa not null constraint on new column with no static default."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card ADD COLUMN id bigint NOT NULL -- noqa: UN011
    ;
    """

    violations: core.ViolationMetric = (
        lint_not_null_constraint_on_new_column_with_no_static_default.run(
            source_path=SOURCE_PATH,
            source_code=sql_pass_noqa,
        )
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_not_null_constraint_on_new_column_with_no_static_default(
    lint_not_null_constraint_on_new_column_with_no_static_default: core.Linter,
) -> None:
    """Test not null constraint on new column with no static default."""
    sql_noqa: str = """
    ALTER TABLE public.card ADD COLUMN id bigint NOT NULL -- noqa: UN002
    ;
    """

    violations: core.ViolationMetric = (
        lint_not_null_constraint_on_new_column_with_no_static_default.run(
            source_path=SOURCE_PATH,
            source_code=sql_noqa,
        )
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_not_null_constraint_on_new_column_with_no_static_default(
    lint_not_null_constraint_on_new_column_with_no_static_default: core.Linter,
) -> None:
    """Test fail noqa not null constraint on new column with no static default."""
    sql_noqa: str = """
    ALTER TABLE public.card ADD COLUMN id bigint NOT NULL -- noqa:
    ;
    """

    violations: core.ViolationMetric = (
        lint_not_null_constraint_on_new_column_with_no_static_default.run(
            source_path=SOURCE_PATH,
            source_code=sql_noqa,
        )
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
