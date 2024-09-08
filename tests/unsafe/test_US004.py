"""Test adding auto increment column."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.US004 import AddingAutoIncrementColumn


@pytest.fixture(scope="module")
def adding_auto_increment_column() -> core.BaseChecker:
    """Create an instance of AddingAutoIncrementColumn."""
    return AddingAutoIncrementColumn()


@pytest.fixture
def lint_adding_auto_increment_column(
    linter: core.Linter,
    adding_auto_increment_column: core.BaseChecker,
) -> core.Linter:
    """Lint AddingAutoIncrementColumn."""
    linter.checkers.add(adding_auto_increment_column)

    return linter


def test_adding_auto_increment_column_rule_code(
    adding_auto_increment_column: core.BaseChecker,
) -> None:
    """Test adding auto increment column rule code."""
    assert (
        adding_auto_increment_column.code
        == adding_auto_increment_column.__module__.split(".")[-1]
    )


def test_adding_auto_increment_column_auto_fixable(
    adding_auto_increment_column: core.BaseChecker,
) -> None:
    """Test adding auto increment column auto fixable."""
    assert adding_auto_increment_column.is_auto_fixable is False


def test_fail_adding_small_serial_column(
    lint_adding_auto_increment_column: core.Linter,
) -> None:
    """Test fail adding small serial column."""
    sql_fail: str = """
    ALTER TABLE public.card ADD COLUMN id smallserial
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_adding_serial_column(
    lint_adding_auto_increment_column: core.Linter,
) -> None:
    """Test fail adding serial column."""
    sql_fail: str = """
    ALTER TABLE public.card ADD COLUMN id serial;
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_adding_big_serial_column(
    lint_adding_auto_increment_column: core.Linter,
) -> None:
    """Test fail adding big serial column."""
    sql_fail: str = """
    ALTER TABLE public.card ADD COLUMN id bigserial
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_adding_auto_increment_column_description(
    lint_adding_auto_increment_column: core.Linter,
    adding_auto_increment_column: core.BaseChecker,
) -> None:
    """Test fail adding auto increment column description."""
    sql_fail: str = """
    ALTER TABLE public.card ADD COLUMN id serial
    ;
    """

    _: core.ViolationMetric = lint_adding_auto_increment_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(iter(adding_auto_increment_column.violations)).description
        == "Forbid adding auto increment column"
    )


def test_pass_noqa_adding_auto_increment_column(
    lint_adding_auto_increment_column: core.Linter,
) -> None:
    """Test pass noqa adding auto increment column."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card ADD COLUMN id serial -- noqa: US004
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_adding_auto_increment_column(
    lint_adding_auto_increment_column: core.Linter,
) -> None:
    """Test fail noqa adding auto increment column."""
    sql_noqa: str = """
    ALTER TABLE public.card ADD COLUMN id serial -- noqa: US002
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_adding_auto_increment_column(
    lint_adding_auto_increment_column: core.Linter,
) -> None:
    """Test fail noqa adding auto increment column."""
    sql_noqa: str = """
    ALTER TABLE public.card ADD COLUMN id serial -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_adding_auto_increment_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
