"""Test drop tablespace."""

from pgshield import core
from pgshield.rules.unsafe.UN007 import DropTablespace


def test_drop_tablespace(linter: core.Linter) -> None:
    """Test drop tablespace."""
    fail_sql: str = """
    DROP TABLESPACE test;
    """

    drop_tablespace: core.Checker = DropTablespace()

    assert drop_tablespace.is_auto_fixable is False

    assert drop_tablespace.code == drop_tablespace.__module__.split(".")[-1]

    linter.checkers.add(drop_tablespace)

    violations: core.ViolationMetric = linter.run(
        source_path="test.sql", source_code=fail_sql,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )

    assert (
        next(iter(drop_tablespace.violations)).description == "Drop tablespace detected"
    )
