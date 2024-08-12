"""Test validated foreign key constraint on existing rows."""

from pgshield import core
from pgshield.rules.unsafe.UN012 import ValidatedForeignKeyConstraintOnExistingRows


def test_validated_foreign_key_constraint_on_existing_rows() -> None:
    """Test validated foreign key constraint on existing rows."""
    fail_sql: str = """
    ALTER TABLE public.card
        ADD CONSTRAINT fkey FOREIGN KEY(account_id) REFERENCES public.account(id)
    ;
    """

    fix_sql: str = "ALTER TABLE public.card ADD CONSTRAINT fkey FOREIGN KEY (account_id) REFERENCES public.account (id) NOT VALID ;"  # noqa: E501

    config: core.Config = core.parse_config()

    core.Checker.config = config

    validated_foreign_key_constraint_on_existing_rows: core.Checker = (
        ValidatedForeignKeyConstraintOnExistingRows()
    )

    linter: core.Linter = core.Linter(config=config)

    assert validated_foreign_key_constraint_on_existing_rows.is_auto_fixable is True

    assert (
        validated_foreign_key_constraint_on_existing_rows.code
        == validated_foreign_key_constraint_on_existing_rows.__module__.split(".")[-1]
    )

    linter.checkers.add(validated_foreign_key_constraint_on_existing_rows)

    validated_foreign_key_constraint_on_existing_rows.config.fix = False

    violations: core.ViolationMetric = linter.run(
        source_path="test.sql", source_code=fail_sql,
    )

    assert violations == core.ViolationMetric(
        violations_total=1,
        violations_fixed_total=0,
        violations_fixable_auto_total=1,
        violations_fixable_manual_total=0,
        violations_fixes=None,
    )

    assert (
        next(
            iter(validated_foreign_key_constraint_on_existing_rows.violations),
        ).description
        == "Validated foreign key constraint on existing rows"
    )

    validated_foreign_key_constraint_on_existing_rows.config.fix = True

    violations = linter.run(
        source_path="test.sql", source_code=fail_sql,
    )

    assert violations == core.ViolationMetric(
        violations_total=1,
        violations_fixed_total=1,
        violations_fixable_auto_total=1,
        violations_fixable_manual_total=0,
        violations_fixes=fix_sql,
    )
