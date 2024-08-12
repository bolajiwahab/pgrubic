"""Test column data type change."""

from pgshield import core
from pgshield.rules.unsafe.UN002 import ColumnDataTypeChange


def test_column_data_type_change() -> None:
    """Test column data type change."""
    fail_sql: str = """
    ALTER TABLE public.card ALTER COLUMN id TYPE bigint;
    """

    column_data_type_change: core.Checker = ColumnDataTypeChange()

    config: core.Config = core.parse_config()

    linter: core.Linter = core.Linter(config=config)

    assert column_data_type_change.is_auto_fixable is False

    assert (
        column_data_type_change.code
        == column_data_type_change.__module__.split(".")[-1]
    )

    linter.checkers.add(column_data_type_change)

    violations: core.ViolationMetric = linter.run(
        source_path="test.sql", source_code=fail_sql,
    )

    assert violations == core.ViolationMetric(
        violations_total=1,
        violations_fixed_total=0,
        violations_fixable_auto_total=0,
        violations_fixable_manual_total=1,
    )

    assert (
        next(iter(column_data_type_change.violations)).description
        == "Forbid column type change"
    )
