"""Test UN001."""
from pgshield import core
from pgshield.rules.unsafe import UN001


def test_UN001() -> None:
    """Test UN001."""
    sql = """
    ALTER TABLE public.ecdict DROP COLUMN id;
    """
    config: core.Config = core.parse_config()
    linter: core.Linter = core.Linter(config=config)
    UN001.DropColumn.code = "UN001"
    assert UN001.DropColumn.is_auto_fixable is False
    linter.checkers.add(UN001.DropColumn())
    violations = linter.run(source_path="test.sql", source_code=sql)
    assert violations.violations_total == 1
    assert violations.violations_fixed_total == 0
    assert violations.violations_fixable_auto_total == 0
    assert violations.violations_fixable_manual_total == 1
