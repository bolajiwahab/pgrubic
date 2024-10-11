"""Test primary key constraint creating new index."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.US015 import PrimaryKeyConstraintCreatingNewIndex


@pytest.fixture(scope="module")
def primary_key_constraint_creating_new_index() -> core.BaseChecker:
    """Create an instance of PrimaryKeyConstraintCreatingNewIndex."""
    core.add_set_locations_to_rule(PrimaryKeyConstraintCreatingNewIndex)
    return PrimaryKeyConstraintCreatingNewIndex()


@pytest.fixture
def lint_primary_key_constraint_creating_new_index(
    linter: core.Linter,
    primary_key_constraint_creating_new_index: core.BaseChecker,
) -> core.Linter:
    """Lint PrimaryKeyConstraintCreatingNewIndex."""
    linter.checkers.add(primary_key_constraint_creating_new_index)

    return linter


def test_primary_key_constraint_creating_new_index_rule_code(
    primary_key_constraint_creating_new_index: core.BaseChecker,
) -> None:
    """Test primary key constraint creating new index rule code."""
    assert (
        primary_key_constraint_creating_new_index.code
        == primary_key_constraint_creating_new_index.__module__.split(
            ".",
        )[-1]
    )


def test_primary_key_constraint_creating_new_index_auto_fixable(
    primary_key_constraint_creating_new_index: core.BaseChecker,
) -> None:
    """Test primary key constraint creating new index auto fixable."""
    assert primary_key_constraint_creating_new_index.is_auto_fixable is False


def test_pass_primary_key_constraint_creating_new_index(
    lint_primary_key_constraint_creating_new_index: core.Linter,
) -> None:
    """Test primary key constraint creating new index."""
    sql_pass: str = """
    ALTER TABLE public.card
        ADD CONSTRAINT unq PRIMARY KEY USING INDEX unq
    ;
    """

    violations: core.ViolationMetric = lint_primary_key_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_primary_key_constraint_creating_new_index(
    lint_primary_key_constraint_creating_new_index: core.Linter,
) -> None:
    """Test primary key constraint creating new index."""
    sql_fail: str = """
    ALTER TABLE public.card ADD CONSTRAINT unq PRIMARY KEY(account_id);
    """

    violations: core.ViolationMetric = lint_primary_key_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_primary_key_constraint_creating_new_index_description(
    lint_primary_key_constraint_creating_new_index: core.Linter,
    primary_key_constraint_creating_new_index: core.BaseChecker,
) -> None:
    """Test primary key constraint creating new index description."""
    sql_fail: str = """
    ALTER TABLE public.card ADD CONSTRAINT unq PRIMARY KEY(account_id);
    """

    _: core.ViolationMetric = lint_primary_key_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(primary_key_constraint_creating_new_index.violations),
        ).description
        == "Primary key constraint creating new index"
    )


def test_pass_noqa_primary_key_constraint_creating_new_index(
    lint_primary_key_constraint_creating_new_index: core.Linter,
) -> None:
    """Test pass noqa primary key constraint creating new index."""
    sql_pass_noqa: str = """
    -- noqa: US015
    ALTER TABLE public.card ADD CONSTRAINT unq PRIMARY KEY(account_id);
    """

    violations: core.ViolationMetric = lint_primary_key_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_primary_key_constraint_creating_new_index(
    lint_primary_key_constraint_creating_new_index: core.Linter,
) -> None:
    """Test fail noqa primary key constraint creating new index."""
    sql_noqa: str = """
    -- noqa: US001
    ALTER TABLE public.card ADD CONSTRAINT unq PRIMARY KEY(account_id);
    """

    violations: core.ViolationMetric = lint_primary_key_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_primary_key_constraint_creating_new_index(
    lint_primary_key_constraint_creating_new_index: core.Linter,
) -> None:
    """Test pass noqa primary key constraint creating new index."""
    sql_noqa: str = """
    -- noqa:
    ALTER TABLE public.card ADD CONSTRAINT unq PRIMARY KEY(account_id);
    """

    violations: core.ViolationMetric = lint_primary_key_constraint_creating_new_index.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
