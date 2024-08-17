"""Test drop schema."""

from pgshield import core
from pgshield.rules.unsafe.UN009 import DropSchema


def test_drop_schema(linter: core.Linter) -> None:
    """Test drop schema."""
    fail_sql: str = """
    DROP SCHEMA test;
    """

    drop_schema: core.Checker = DropSchema()

    assert drop_schema.is_auto_fixable is False

    assert drop_schema.code == drop_schema.__module__.split(".")[-1]

    linter.checkers.add(drop_schema)

    violations: core.ViolationMetric = linter.run(
        source_path="test.sql", source_code=fail_sql,
    )

    assert violations == core.ViolationMetric(
        violations_total=1,
        violations_fixed_total=0,
        violations_fixable_auto_total=0,
        violations_fixable_manual_total=1,
    )

    assert next(iter(drop_schema.violations)).description == "Drop schema detected"
