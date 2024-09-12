"""Test unique constraint creating new index."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.US014 import UniqueConstraintCreatingNewIndex


@pytest.fixture(scope="module")
def unique_constraint_creating_new_index() -> core.BaseChecker:
    """Create an instance of UniqueConstraintCreatingNewIndex."""
    core.add_set_locations_to_rule(UniqueConstraintCreatingNewIndex)
    return UniqueConstraintCreatingNewIndex()


@pytest.fixture
def lint_unique_constraint_creating_new_index(
    linter: core.Linter,
    unique_constraint_creating_new_index: core.BaseChecker,
) -> core.Linter:
    """Lint UniqueConstraintCreatingNewIndex."""
    linter.checkers.add(unique_constraint_creating_new_index)

    return linter


def test_unique_constraint_creating_new_index_rule_code(
    unique_constraint_creating_new_index: core.BaseChecker,
) -> None:
    """Test unique constraint creating new index rule code."""
    assert (
        unique_constraint_creating_new_index.code
        == unique_constraint_creating_new_index.__module__.split(
            ".",
        )[-1]
    )


def test_unique_constraint_creating_new_index_auto_fixable(
    unique_constraint_creating_new_index: core.BaseChecker,
) -> None:
    """Test unique constraint creating new index auto fixable."""
    assert unique_constraint_creating_new_index.is_auto_fixable is False


def test_pass_unique_constraint_creating_new_index(
    lint_unique_constraint_creating_new_index: core.Linter,
) -> None:
    """Test unique constraint creating new index."""
    sql_pass: str = """
    ALTER TABLE public.card
        ADD CONSTRAINT unq UNIQUE USING INDEX unq
    ;
    """

    violations: core.ViolationMetric = lint_unique_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_unique_constraint_creating_new_index(
    lint_unique_constraint_creating_new_index: core.Linter,
) -> None:
    """Test unique constraint creating new index."""
    sql_fail: str = """
    ALTER TABLE public.card ADD CONSTRAINT unq UNIQUE(account_id);
    """

    violations: core.ViolationMetric = lint_unique_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_unique_constraint_creating_new_index_description(
    lint_unique_constraint_creating_new_index: core.Linter,
    unique_constraint_creating_new_index: core.BaseChecker,
) -> None:
    """Test unique constraint creating new index description."""
    sql_fail: str = """
    ALTER TABLE public.card ADD CONSTRAINT unq UNIQUE(account_id);
    """

    _: core.ViolationMetric = lint_unique_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(unique_constraint_creating_new_index.violations),
        ).description
        == "Unique constraint creating new index"
    )


def test_pass_noqa_unique_constraint_creating_new_index(
    lint_unique_constraint_creating_new_index: core.Linter,
) -> None:
    """Test pass noqa unique constraint creating new index."""
    sql_pass_noqa: str = """
    -- noqa: US014
    ALTER TABLE public.card ADD CONSTRAINT unq UNIQUE(account_id);
    """

    violations: core.ViolationMetric = lint_unique_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_unique_constraint_creating_new_index(
    lint_unique_constraint_creating_new_index: core.Linter,
) -> None:
    """Test fail noqa unique constraint creating new index."""
    sql_noqa: str = """
    -- noqa: US001
    ALTER TABLE public.card ADD CONSTRAINT unq UNIQUE(account_id);
    """

    violations: core.ViolationMetric = lint_unique_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_unique_constraint_creating_new_index(
    lint_unique_constraint_creating_new_index: core.Linter,
) -> None:
    """Test pass noqa unique constraint creating new index."""
    sql_noqa: str = """
    -- noqa:
    ALTER TABLE public.card ADD CONSTRAINT unq UNIQUE(account_id);
    """

    violations: core.ViolationMetric = lint_unique_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
