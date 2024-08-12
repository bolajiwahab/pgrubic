"""Test drop column."""

from pgshield import core
from pgshield.rules.unsafe.UN001 import DropColumn


def test_drop_column() -> None:
    """Test drop column."""
    fail_sql: str = """
    ALTER TABLE public.card DROP COLUMN id;
    """

    drop_column: core.Checker = DropColumn()

    config: core.Config = core.parse_config()

    linter: core.Linter = core.Linter(config=config)

    assert drop_column.is_auto_fixable is False

    assert drop_column.code == drop_column.__module__.split(".")[-1]

    linter.checkers.add(drop_column)

    violations: core.ViolationMetric = linter.run(
        source_path="test.sql", source_code=fail_sql,
    )

    assert violations == core.ViolationMetric(
        violations_total=1,
        violations_fixed_total=0,
        violations_fixable_auto_total=0,
        violations_fixable_manual_total=1,
    )

    assert next(iter(drop_column.violations)).description == "Drop column detected"
