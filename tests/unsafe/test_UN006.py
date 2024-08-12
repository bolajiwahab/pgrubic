"""Test adding auto increment column."""

from pgshield import core
from pgshield.rules.unsafe.UN006 import AddingStoredGeneratedColumn


def test_adding_auto_increment_column() -> None:
    """Test adding auto increment column."""
    fail_sql: str = """
    ALTER TABLE public.card
        ADD COLUMN id bigint GENERATED ALWAYS AS (id / 10) STORED
    ;
    """

    adding_auto_increment_column: core.Checker = AddingStoredGeneratedColumn()

    config: core.Config = core.parse_config()

    linter: core.Linter = core.Linter(config=config)

    assert adding_auto_increment_column.is_auto_fixable is False

    assert (
        adding_auto_increment_column.code
        == adding_auto_increment_column.__module__.split(".")[-1]
    )

    linter.checkers.add(adding_auto_increment_column)

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
        next(iter(adding_auto_increment_column.violations)).description
        == "Forbid adding stored generated column"
    )
