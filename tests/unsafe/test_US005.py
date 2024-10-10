"""Test adding auto increment column."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US005 import AddingAutoIncrementIdentityColumn


@pytest.fixture(scope="module")
def adding_auto_increment_identity_column() -> core.BaseChecker:
    """Create an instance of AddingAutoIncrementIdentityColumn."""
    core.add_set_locations_to_rule(AddingAutoIncrementIdentityColumn)
    return AddingAutoIncrementIdentityColumn()


@pytest.fixture
def lint_adding_auto_increment_identity_column(
    linter: core.Linter,
    adding_auto_increment_identity_column: core.BaseChecker,
) -> core.Linter:
    """Lint AddingAutoIncrementIdentityColumn."""
    linter.checkers.add(adding_auto_increment_identity_column)

    return linter


def test_adding_auto_increment_identity_column_rule_code(
    adding_auto_increment_identity_column: core.BaseChecker,
) -> None:
    """Test adding auto increment identity column rule code."""
    assert (
        adding_auto_increment_identity_column.code
        == adding_auto_increment_identity_column.__module__.split(".")[-1]
    )


def test_adding_auto_increment_identity_column_auto_fixable(
    adding_auto_increment_identity_column: core.BaseChecker,
) -> None:
    """Test adding auto increment identity column auto fixable."""
    assert adding_auto_increment_identity_column.is_auto_fixable is False


def test_fail_adding_auto_increment_identity_column(
    lint_adding_auto_increment_identity_column: core.Linter,
) -> None:
    """Test fail adding auto increment identity column."""
    sql_fail: str = """
    ALTER TABLE public.card ADD COLUMN id bigint GENERATED ALWAYS AS IDENTITY
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_identity_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_adding_auto_increment_identity_column_description(
    lint_adding_auto_increment_identity_column: core.Linter,
    adding_auto_increment_identity_column: core.BaseChecker,
) -> None:
    """Test fail adding auto increment identity column description."""
    sql_fail: str = """
    ALTER TABLE public.card ADD COLUMN id bigint GENERATED ALWAYS AS IDENTITY
    ;
    """

    _: core.ViolationMetric = lint_adding_auto_increment_identity_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(iter(adding_auto_increment_identity_column.violations)).description
        == "Forbid adding auto increment identity column"
    )


def test_pass_noqa_adding_auto_increment_identity_column(
    lint_adding_auto_increment_identity_column: core.Linter,
) -> None:
    """Test pass noqa adding auto increment identity column."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card
        ADD COLUMN id bigint GENERATED ALWAYS AS IDENTITY -- noqa: US005
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_identity_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_adding_auto_increment_identity_column(
    lint_adding_auto_increment_identity_column: core.Linter,
) -> None:
    """Test fail noqa adding auto increment identity column."""
    sql_noqa: str = """
    ALTER TABLE public.card
        ADD COLUMN id bigint GENERATED ALWAYS AS IDENTITY -- noqa: US002
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_identity_column.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_adding_auto_increment_identity_column(
    lint_adding_auto_increment_identity_column: core.Linter,
) -> None:
    """Test fail noqa adding auto increment identity column."""
    sql_noqa: str = """
    ALTER TABLE public.card ADD COLUMN id bigint GENERATED ALWAYS AS IDENTITY -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_identity_column.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
