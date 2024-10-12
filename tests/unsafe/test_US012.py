"""Test validating foreign key constraint on existing rows."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US012 import ValidatingForeignKeyConstraintOnExistingRows


@pytest.fixture(scope="module")
def validating_foreign_key_constraint_on_existing_rows() -> core.BaseChecker:
    """Create an instance of ValidatingForeignKeyConstraintOnExistingRows."""
    core.add_apply_fix_to_rule(ValidatingForeignKeyConstraintOnExistingRows)
    core.add_set_locations_to_rule(ValidatingForeignKeyConstraintOnExistingRows)
    return ValidatingForeignKeyConstraintOnExistingRows()


@pytest.fixture
def lint_validating_foreign_key_constraint_on_existing_rows(
    linter: core.Linter,
    validating_foreign_key_constraint_on_existing_rows: core.BaseChecker,
) -> core.Linter:
    """Lint ValidatingForeignKeyConstraintOnExistingRows."""
    validating_foreign_key_constraint_on_existing_rows.config.lint.fix = False
    linter.checkers.add(validating_foreign_key_constraint_on_existing_rows)

    return linter


def test_validating_foreign_key_constraint_on_existing_rows_rule_code(
    validating_foreign_key_constraint_on_existing_rows: core.BaseChecker,
) -> None:
    """Test validating foreign key constraint on existing rows rule code."""
    assert (
        validating_foreign_key_constraint_on_existing_rows.code
        == validating_foreign_key_constraint_on_existing_rows.__module__.split(
            ".",
        )[-1]
    )


def test_validating_foreign_key_constraint_on_existing_rows_auto_fixable(
    validating_foreign_key_constraint_on_existing_rows: core.BaseChecker,
) -> None:
    """Test validating foreign key constraint on existing rows auto fixable."""
    assert validating_foreign_key_constraint_on_existing_rows.is_auto_fixable is True


def test_pass_validating_foreign_key_constraint_on_existing_rows(
    lint_validating_foreign_key_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test validating foreign key constraint on existing rows."""
    sql_pass: str = """
    ALTER TABLE public.card
        ADD CONSTRAINT fkey FOREIGN KEY(account_id) REFERENCES public.account(id)
        NOT VALID
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_foreign_key_constraint_on_existing_rows.run(
            source_file=TEST_FILE,
            source_code=sql_pass,
        )
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_validating_foreign_key_constraint_on_existing_rows(
    lint_validating_foreign_key_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test validating foreign key constraint on existing rows."""
    sql_fail: str = """
    ALTER TABLE public.card
        ADD CONSTRAINT fkey FOREIGN KEY(account_id) REFERENCES public.account(id)
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_foreign_key_constraint_on_existing_rows.run(
            source_file=TEST_FILE,
            source_code=sql_fail,
        )
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_validating_foreign_key_constraint_on_existing_rows_description(
    lint_validating_foreign_key_constraint_on_existing_rows: core.Linter,
    validating_foreign_key_constraint_on_existing_rows: core.BaseChecker,
) -> None:
    """Test validating foreign key constraint on existing rows description."""
    sql_fail: str = """
    ALTER TABLE public.card
        ADD CONSTRAINT fkey FOREIGN KEY(account_id) REFERENCES public.account(id)
    ;
    """

    _: core.ViolationMetric = lint_validating_foreign_key_constraint_on_existing_rows.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(validating_foreign_key_constraint_on_existing_rows.violations),
        ).description
        == "Validating foreign key constraint on existing rows"
    )


def test_pass_noqa_validating_foreign_key_constraint_on_existing_rows(
    lint_validating_foreign_key_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test pass noqa validating foreign key constraint on existing rows."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card -- noqa: US012
        ADD CONSTRAINT fkey FOREIGN KEY(account_id) REFERENCES public.account(id)
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_foreign_key_constraint_on_existing_rows.run(
            source_file=TEST_FILE,
            source_code=sql_pass_noqa,
        )
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_validating_foreign_key_constraint_on_existing_rows(
    lint_validating_foreign_key_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test validating foreign key constraint on existing rows."""
    sql_noqa: str = """
    ALTER TABLE public.card -- noqa: US013
        ADD CONSTRAINT fkey FOREIGN KEY(account_id) REFERENCES public.account(id)
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_foreign_key_constraint_on_existing_rows.run(
            source_file=TEST_FILE,
            source_code=sql_noqa,
        )
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_validating_foreign_key_constraint_on_existing_rows(
    lint_validating_foreign_key_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test fail noqa validating foreign key constraint on existing rows."""
    sql_noqa: str = """
    ALTER TABLE public.card -- noqa
        ADD CONSTRAINT fkey FOREIGN KEY(account_id) REFERENCES public.account(id)
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_foreign_key_constraint_on_existing_rows.run(
            source_file=TEST_FILE,
            source_code=sql_noqa,
        )
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_validating_foreign_key_constraint_on_existing_rows(
    lint_validating_foreign_key_constraint_on_existing_rows: core.Linter,
    validating_foreign_key_constraint_on_existing_rows: core.BaseChecker,
) -> None:
    """Test fail fix validating foreign key constraint on existing rows."""
    sql_fail: str = """
    ALTER TABLE public.card
        ADD CONSTRAINT fkey FOREIGN KEY(account_id) REFERENCES public.account(id)
    ;
    """

    sql_fix: str = "ALTER TABLE public.card\n    ADD CONSTRAINT fkey FOREIGN KEY (account_id) REFERENCES public.account (id) NOT VALID ;"  # noqa: E501

    validating_foreign_key_constraint_on_existing_rows.config.lint.fix = True

    violations: core.ViolationMetric = (
        lint_validating_foreign_key_constraint_on_existing_rows.run(
            source_file=TEST_FILE,
            source_code=sql_fail,
        )
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
