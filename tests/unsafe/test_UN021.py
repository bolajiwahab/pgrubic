"""Test drop table."""

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.UN021 import DropTable


def test_drop_table() -> None:
    """Test drop table."""
    sql: str = """
    DROP TABLE public.card;
    """
    drop_table: core.BaseChecker = DropTable()
    config: core.Config = core.parse_config()
    linter: core.Linter = core.Linter(config=config)
    assert drop_table.is_auto_fixable is False
    assert drop_table.code == drop_table.__module__.split(".")[-1]
    linter.checkers.add(drop_table)
    violations: core.ViolationMetric = linter.run(
        source_path=SOURCE_PATH,
        source_code=sql,
    )
    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )
    assert next(iter(drop_table.violations)).description == "Drop table found"
