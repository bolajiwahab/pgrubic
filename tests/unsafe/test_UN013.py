"""Test validating check constraint on existing rows."""

import pytest

from pgshield import core
from pgshield.rules.unsafe.UN013 import ValidatingCheckConstraintOnExistingRows


@pytest.fixture(scope="module")
def validating_check_constraint_on_existing_rows() -> core.Checker:
    """Create an instance of ValidatingCheckConstraintOnExistingRows."""
    return ValidatingCheckConstraintOnExistingRows()


@pytest.fixture()
def lint_validating_check_constraint_on_existing_rows(
    linter: core.Linter,
    validating_check_constraint_on_existing_rows: core.Checker,
) -> core.Linter:
    """Lint ValidatingCheckConstraintOnExistingRows."""
    validating_check_constraint_on_existing_rows.config.fix = False
    linter.checkers.add(validating_check_constraint_on_existing_rows)

    return linter


def test_validating_check_constraint_on_existing_rows_rule_code(
    validating_check_constraint_on_existing_rows: core.Checker,
) -> None:
    """Test validating check constraint on existing rows rule code."""
    assert (
        validating_check_constraint_on_existing_rows.code
        == validating_check_constraint_on_existing_rows.__module__.split(
            ".",
        )[-1]
    )


def test_validating_check_constraint_on_existing_rows_auto_fixable(
    validating_check_constraint_on_existing_rows: core.Checker,
) -> None:
    """Test validating check constraint on existing rows auto fixable."""
    assert (
        validating_check_constraint_on_existing_rows.is_auto_fixable
        is True
    )


def test_pass_validating_check_constraint_on_existing_rows(
    lint_validating_check_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test validating check constraint on existing rows."""
    sql_pass: str = """
    ALTER TABLE public.card
        ADD CONSTRAINT chk CHECK(account_id > 0) NOT VALID
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_check_constraint_on_existing_rows.run(
            source_path="test.sql",
            source_code=sql_pass,
        )
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_validating_check_constraint_on_existing_rows(
    lint_validating_check_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test validating check constraint on existing rows."""
    sql_fail: str = """
    ALTER TABLE public.card ADD CONSTRAINT chk CHECK(account_id > 0)
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_check_constraint_on_existing_rows.run(
            source_path="test.sql",
            source_code=sql_fail,
        )
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_validating_check_constraint_on_existing_rows_description(
    lint_validating_check_constraint_on_existing_rows: core.Linter,
    validating_check_constraint_on_existing_rows: core.Checker,
) -> None:
    """Test validating check constraint on existing rows description."""
    sql_fail: str = """
    ALTER TABLE public.card ADD CONSTRAINT chk CHECK(account_id > 0)
    ;
    """

    _: core.ViolationMetric = (
        lint_validating_check_constraint_on_existing_rows.run(
            source_path="test.sql",
            source_code=sql_fail,
        )
    )

    assert (
        next(
            iter(validating_check_constraint_on_existing_rows.violations),
        ).description
        == "Validating check constraint on existing rows"
    )


def test_pass_noqa_validating_check_constraint_on_existing_rows(
    lint_validating_check_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test pass noqa validating check constraint on existing rows."""
    sql_pass_noqa: str = """
    ALTER TABLE public.card -- noqa: UN013
        ADD CONSTRAINT chk CHECK(account_id > 0)
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_check_constraint_on_existing_rows.run(
            source_path="test.sql",
            source_code=sql_pass_noqa,
        )
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_validating_check_constraint_on_existing_rows(
    lint_validating_check_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test validating check constraint on existing rows."""
    sql_noqa: str = """
    ALTER TABLE public.card -- noqa: UN014
        ADD CONSTRAINT chk CHECK(account_id > 0)
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_check_constraint_on_existing_rows.run(
            source_path="test.sql",
            source_code=sql_noqa,
        )
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_validating_check_constraint_on_existing_rows(
    lint_validating_check_constraint_on_existing_rows: core.Linter,
) -> None:
    """Test fail noqa validating check constraint on existing rows."""
    sql_noqa: str = """
    ALTER TABLE public.card -- noqa:
        ADD CONSTRAINT chk CHECK(account_id > 0)
    ;
    """

    violations: core.ViolationMetric = (
        lint_validating_check_constraint_on_existing_rows.run(
            source_path="test.sql",
            source_code=sql_noqa,
        )
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_validating_check_constraint_on_existing_rows(
    lint_validating_check_constraint_on_existing_rows: core.Linter,
    validating_check_constraint_on_existing_rows: core.Checker,
) -> None:
    """Test fail fix validating check constraint on existing rows."""
    sql_fail: str = """
    ALTER TABLE public.card
        ADD CONSTRAINT chk CHECK(account_id > 0)
    ;
    """

    sql_fix: str = (
        "ALTER TABLE public.card ADD CONSTRAINT chk CHECK (account_id > 0) NOT VALID ;"
    )

    validating_check_constraint_on_existing_rows.config.fix = True

    violations: core.ViolationMetric = (
        lint_validating_check_constraint_on_existing_rows.run(
            source_path="test.sql",
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
