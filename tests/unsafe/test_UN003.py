"""Test column rename."""

from pgshield import core
from pgshield.rules.unsafe.UN003 import ColumnRename


def test_column_rename(linter: core.Linter) -> None:
    """Test column data type change."""
    fail_sql: str = """
    ALTER TABLE public.card RENAME COLUMN id TO card_id;
    """

    column_rename: core.Checker = ColumnRename()

    assert column_rename.is_auto_fixable is False

    assert column_rename.code == column_rename.__module__.split(".")[-1]

    linter.checkers.add(column_rename)

    violations: core.ViolationMetric = linter.run(
        source_path="test.sql", source_code=fail_sql,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )

    assert next(iter(column_rename.violations)).description == "Forbid column rename"
