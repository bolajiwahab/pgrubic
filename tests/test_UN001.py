"""Test UN001."""

from pgshield import core
from pgshield.rules.unsafe import UN001


def test_UN001() -> None:
    """Test drop column."""
    sql = """
    ALTER TABLE public.ecdict DROP COLUMN id;
    """
    drop_column = UN001.DropColumn()
    config: core.Config = core.parse_config()
    linter: core.Linter = core.Linter(config=config)
    assert drop_column.is_auto_fixable is False
    assert drop_column.code == "UN001"
    linter.checkers.add(drop_column)
    violations = linter.run(source_path="test.sql", source_code=sql)
    assert violations == core.ViolationMetric(
        violations_total=1,
        violations_fixed_total=0,
        violations_fixable_auto_total=0,
        violations_fixable_manual_total=1,
    )
    assert next(iter(drop_column.violations)).description == "Drop column found"
