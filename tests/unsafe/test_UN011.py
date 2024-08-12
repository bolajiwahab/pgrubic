"""Test not null constraint on new column with no static default."""

from pgshield import core
from pgshield.rules.unsafe.UN011 import NotNullConstraintOnNewColumnWithNoStaticDefault


def test_not_null_constraint_on_new_column_with_no_static_default() -> None:
    """Test not null constraint on new column with no static default."""
    pass_sql: str = """
    ALTER TABLE public.card ADD COLUMN id bigint NOT NULL DEFAULT 0;
    """

    fail_sql: str = """
    ALTER TABLE public.card ADD COLUMN id bigint NOT NULL;
    """

    not_null_constraint_on_new_column_with_no_static_default: core.Checker = (
        NotNullConstraintOnNewColumnWithNoStaticDefault()
    )

    config: core.Config = core.parse_config()

    linter: core.Linter = core.Linter(config=config)

    assert (
        not_null_constraint_on_new_column_with_no_static_default.is_auto_fixable
        is False
    )

    assert (
        not_null_constraint_on_new_column_with_no_static_default.code
        == not_null_constraint_on_new_column_with_no_static_default.__module__.split(
            ".",
        )[-1]
    )

    linter.checkers.add(not_null_constraint_on_new_column_with_no_static_default)

    violations: core.ViolationMetric = linter.run(
        source_path="test.sql", source_code=pass_sql,
    )

    assert violations == core.ViolationMetric(
        violations_total=0,
        violations_fixed_total=0,
        violations_fixable_auto_total=0,
        violations_fixable_manual_total=0,
    )

    violations = linter.run(
        source_path="test.sql", source_code=fail_sql,
    )

    assert violations == core.ViolationMetric(
        violations_total=1,
        violations_fixed_total=0,
        violations_fixable_auto_total=0,
        violations_fixable_manual_total=1,
    )

    assert (
        next(
            iter(not_null_constraint_on_new_column_with_no_static_default.violations),
        ).description
        == "Not null constraint on new column with no static default"
    )
