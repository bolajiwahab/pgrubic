"""Test drop database."""

from pgshield import core
from pgshield.rules.unsafe.UN008 import DropDatabase


def test_drop_database(linter: core.Linter) -> None:
    """Test drop database."""
    fail_sql: str = """
    DROP DATABASE test;
    """

    drop_database: core.Checker = DropDatabase()

    assert drop_database.is_auto_fixable is False

    assert drop_database.code == drop_database.__module__.split(".")[-1]

    linter.checkers.add(drop_database)

    violations: core.ViolationMetric = linter.run(
        source_path="test.sql", source_code=fail_sql,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )

    assert next(iter(drop_database.violations)).description == "Drop database detected"
