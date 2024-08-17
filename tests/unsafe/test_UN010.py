"""Test not null constraint on existing on existing column."""

from pgshield import core
from pgshield.rules.unsafe.UN010 import NotNullConstraintOnExistingColumn


def test_not_null_constraint_on_existing_column(linter: core.Linter) -> None:
    """Test not null constraint on existing column."""
    fail_sql: str = """
    ALTER TABLE public.card ALTER COLUMN id SET NOT NULL;
    """

    not_null_constraint_on_existing_column: core.Checker = (
        NotNullConstraintOnExistingColumn()
    )

    assert not_null_constraint_on_existing_column.is_auto_fixable is False

    assert (
        not_null_constraint_on_existing_column.code
        == not_null_constraint_on_existing_column.__module__.split(".")[-1]
    )

    linter.checkers.add(not_null_constraint_on_existing_column)

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
        next(iter(not_null_constraint_on_existing_column.violations)).description
        == "Not null constraint on existing column"
    )
