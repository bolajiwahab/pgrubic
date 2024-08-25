"""Test column data type change column."""

import pytest

from pgshield import core
from pgshield.rules.unsafe.UN002 import ColumnDataTypeChange


@pytest.fixture(scope="module")
def column_data_type_change() -> core.Checker:
    """Create an instance of ColumnDataTypeChange."""
    return ColumnDataTypeChange()


@pytest.fixture()
def lint_column_data_type_change(
    linter: core.Linter,
    column_data_type_change: core.Checker,
) -> core.Linter:
    """Lint ColumnDataTypeChange."""
    linter.checkers.add(column_data_type_change)

    return linter


def test_column_data_type_change_rule_code(
    column_data_type_change: core.Checker,
) -> None:
    """Test column data type change rule code."""
    assert (
        column_data_type_change.code
        == column_data_type_change.__module__.split(".")[-1]
    )


def test_column_data_type_change_auto_fixable(
    column_data_type_change: core.Checker,
) -> None:
    """Test column data type change auto fixable."""
    assert column_data_type_change.is_auto_fixable is False


def test_fail_column_data_type_change(
    lint_column_data_type_change: core.Linter,
) -> None:
    """Test fail column data type change."""
    sql_fail: str = """
    ALTER TABLE public.card ALTER COLUMN id TYPE bigint
    ;
    """

    violations: core.ViolationMetric = lint_column_data_type_change.run(
        source_path="test.sql",
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_column_data_type_change_description(
    lint_column_data_type_change: core.Linter,
    column_data_type_change: core.Checker,
) -> None:
    """Test fail column data type description."""
    sql_fail: str = """
    ALTER TABLE public.card ALTER COLUMN id TYPE bigint
    ;
    """

    _: core.ViolationMetric = lint_column_data_type_change.run(
        source_path="test.sql",
        source_code=sql_fail,
    )

    assert (
        next(iter(column_data_type_change.violations)).description
        == "Forbid column data type change"
    )


def test_pass_noqa_column_data_type_change(
    lint_column_data_type_change: core.Linter,
) -> None:
    """Test pass noqa column data type change."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card ALTER COLUMN id TYPE bigint -- noqa: UN002
    ;
    """

    violations: core.ViolationMetric = lint_column_data_type_change.run(
        source_path="test.sql",
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_column_data_type_change(
    lint_column_data_type_change: core.Linter,
) -> None:
    """Test fail noqa column data type change."""
    sql_noqa: str = """
    ALTER TABLE public.card ALTER COLUMN id TYPE bigint -- noqa: UN001
    ;
    """

    violations: core.ViolationMetric = lint_column_data_type_change.run(
        source_path="test.sql",
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_column_data_type_change(
    lint_column_data_type_change: core.Linter,
) -> None:
    """Test fail noqa column data type change."""
    sql_noqa: str = """
    ALTER TABLE public.card ALTER COLUMN id TYPE bigint -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_column_data_type_change.run(
        source_path="test.sql",
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )