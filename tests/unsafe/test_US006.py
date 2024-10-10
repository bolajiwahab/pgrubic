"""Test adding generated column."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US006 import AddingStoredGeneratedColumn


@pytest.fixture(scope="module")
def adding_stored_generated_column() -> core.BaseChecker:
    """Create an instance of AddingStoredGeneratedColumn."""
    core.add_set_locations_to_rule(AddingStoredGeneratedColumn)
    return AddingStoredGeneratedColumn()


@pytest.fixture
def lint_adding_stored_generated_column(
    linter: core.Linter,
    adding_stored_generated_column: core.BaseChecker,
) -> core.Linter:
    """Lint AddingStoredGeneratedColumn."""
    linter.checkers.add(adding_stored_generated_column)

    return linter


def test_adding_stored_generated_column_rule_code(
    adding_stored_generated_column: core.BaseChecker,
) -> None:
    """Test adding stored generated column rule code."""
    assert (
        adding_stored_generated_column.code
        == adding_stored_generated_column.__module__.split(".")[-1]
    )


def test_adding_stored_generated_column_auto_fixable(
    adding_stored_generated_column: core.BaseChecker,
) -> None:
    """Test adding stored generated column auto fixable."""
    assert adding_stored_generated_column.is_auto_fixable is False


def test_fail_adding_stored_generated_column(
    lint_adding_stored_generated_column: core.Linter,
) -> None:
    """Test fail adding stored generated column."""
    sql_fail: str = """
    ALTER TABLE public.card
        ADD COLUMN id bigint GENERATED ALWAYS AS (id / 10) STORED
    ;
    """

    violations: core.ViolationMetric = lint_adding_stored_generated_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_adding_stored_generated_column_description(
    lint_adding_stored_generated_column: core.Linter,
    adding_stored_generated_column: core.BaseChecker,
) -> None:
    """Test fail adding stored generated column description."""
    sql_fail: str = """
    ALTER TABLE public.card
        ADD COLUMN id bigint GENERATED ALWAYS AS (id / 10) STORED
    ;
    """

    _: core.ViolationMetric = lint_adding_stored_generated_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(iter(adding_stored_generated_column.violations)).description
        == "Forbid adding stored generated column"
    )


def test_pass_noqa_adding_stored_generated_column(
    lint_adding_stored_generated_column: core.Linter,
) -> None:
    """Test pass noqa adding stored generated column."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card
        ADD COLUMN id bigint GENERATED ALWAYS AS (id / 10) STORED -- noqa: US006
    ;
    """

    violations: core.ViolationMetric = lint_adding_stored_generated_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_adding_stored_generated_column(
    lint_adding_stored_generated_column: core.Linter,
) -> None:
    """Test fail noqa adding stored generated column."""
    sql_noqa: str = """
    ALTER TABLE public.card
        ADD COLUMN id bigint GENERATED ALWAYS AS (id / 10) STORED -- noqa: US002
    ;
    """

    violations: core.ViolationMetric = lint_adding_stored_generated_column.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_adding_stored_generated_column(
    lint_adding_stored_generated_column: core.Linter,
) -> None:
    """Test fail noqa adding stored generated column."""
    sql_noqa: str = """
    ALTER TABLE public.card
        ADD COLUMN id bigint GENERATED ALWAYS AS (id / 10) STORED -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_adding_stored_generated_column.run(
        file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
