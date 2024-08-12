"""Test drop tablespace."""

from pgshield import core
from pgshield.rules.unsafe.UN007 import DropTablespace


def test_drop_tablespace() -> None:
    """Test drop tablespace."""
    fail_sql: str = """
    DROP TABLESPACE test;
    """

    drop_tablespace: core.Checker = DropTablespace()

    config: core.Config = core.parse_config()

    linter: core.Linter = core.Linter(config=config)

    assert drop_tablespace.is_auto_fixable is False

    assert drop_tablespace.code == drop_tablespace.__module__.split(".")[-1]

    linter.checkers.add(drop_tablespace)

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
        next(iter(drop_tablespace.violations)).description == "Drop tablespace detected"
    )
