"""Test removal of constraint."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.constraint.CT004 import RemoveConstraint


@pytest.fixture(scope="module")
def remove_constraint() -> core.BaseChecker:
    """Create an instance of RemoveConstraint."""
    core.add_set_locations_to_rule(RemoveConstraint)
    return RemoveConstraint()


@pytest.fixture
def lint_remove_constraint(
    linter: core.Linter,
    remove_constraint: core.BaseChecker,
) -> core.Linter:
    """Lint RemoveConstraint."""
    linter.checkers.add(remove_constraint)

    return linter


def test_remove_constraint_rule_code(
    remove_constraint: core.BaseChecker,
) -> None:
    """Test remove constraint rule code."""
    assert (
        remove_constraint.code
        == remove_constraint.__module__.split(
            ".",
        )[-1]
    )


def test_remove_constraint_auto_fixable(
    remove_constraint: core.BaseChecker,
) -> None:
    """Test remove constraint auto fixable."""
    assert remove_constraint.is_auto_fixable is False


def test_fail_remove_constraint(
    lint_remove_constraint: core.Linter,
) -> None:
    """Test remove constraint."""
    sql_fail: str = "ALTER TABLE public.card DROP CONSTRAINT card_old;"

    violations: core.ViolationMetric = lint_remove_constraint.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_remove_constraint_description(
    lint_remove_constraint: core.Linter,
    remove_constraint: core.BaseChecker,
) -> None:
    """Test remove constraint description."""
    sql_fail: str = "ALTER TABLE public.card DROP CONSTRAINT card_old;"

    _: core.ViolationMetric = lint_remove_constraint.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(remove_constraint.violations),
        ).description
        == "Constraint `card_old` removal detected"
    )


def test_pass_noqa_remove_constraint(
    lint_remove_constraint: core.Linter,
) -> None:
    """Test pass noqa remove constraint."""
    sql_pass_noqa: str = """
    -- noqa: CT004
    ALTER TABLE public.card DROP CONSTRAINT card_old;
    """

    violations: core.ViolationMetric = lint_remove_constraint.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_remove_constraint(
    lint_remove_constraint: core.Linter,
) -> None:
    """Test fail noqa remove constraint."""
    sql_noqa: str = """
    -- noqa: UN001
    ALTER TABLE public.card DROP CONSTRAINT card_old;
    """

    violations: core.ViolationMetric = lint_remove_constraint.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_remove_constraint(
    lint_remove_constraint: core.Linter,
) -> None:
    """Test pass noqa remove constraint."""
    sql_noqa: str = """
    -- noqa:
    ALTER TABLE public.card DROP CONSTRAINT card_old;
    """

    violations: core.ViolationMetric = lint_remove_constraint.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
