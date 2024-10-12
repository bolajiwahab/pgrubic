"""Test null constraint."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN021 import NullConstraint


@pytest.fixture(scope="module")
def null_constraint() -> core.BaseChecker:
    """Create an instance of NullConstraint."""
    core.add_apply_fix_to_rule(NullConstraint)
    core.add_set_locations_to_rule(NullConstraint)
    return NullConstraint()


@pytest.fixture
def lint_null_constraint(
    linter: core.Linter,
    null_constraint: core.BaseChecker,
) -> core.Linter:
    """Lint NullConstraint."""
    null_constraint.config.lint.fix = False
    linter.checkers.add(null_constraint)

    return linter


def test_null_constraint_rule_code(
    null_constraint: core.BaseChecker,
) -> None:
    """Test null constraint rule code."""
    assert null_constraint.code == null_constraint.__module__.split(".")[-1]


def test_null_constraint_auto_fixable(
    null_constraint: core.BaseChecker,
) -> None:
    """Test null constraint auto fixable."""
    assert null_constraint.is_auto_fixable is True


def test_pass_null_constraintstamp(
    lint_null_constraint: core.Linter,
) -> None:
    """Test pass null constraint."""
    sql_pass: str = "CREATE TABLE tbl (age int NOT NULL);"

    violations: core.ViolationMetric = lint_null_constraint.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_null_constraint(
    lint_null_constraint: core.Linter,
) -> None:
    """Test fail null constraint."""
    sql_fail: str = "CREATE TABLE tbl (age int NULL);"

    violations: core.ViolationMetric = lint_null_constraint.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_null_constraint_description(
    lint_null_constraint: core.Linter,
    null_constraint: core.BaseChecker,
) -> None:
    """Test null constraint description."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN age int NULL;"

    _: core.ViolationMetric = lint_null_constraint.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(null_constraint.violations),
        ).description
        == "NULL constraints are redundant"
    )


def test_pass_noqa_null_constraint(
    lint_null_constraint: core.Linter,
) -> None:
    """Test pass noqa null constraint."""
    sql_pass_noqa: str = """
    -- noqa: GN021
    CREATE TABLE tbl (age int NULL);
    """

    violations: core.ViolationMetric = lint_null_constraint.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_null_constraint(
    lint_null_constraint: core.Linter,
) -> None:
    """Test fail noqa null constraint."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN age int NULL;
    """

    violations: core.ViolationMetric = lint_null_constraint.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_null_constraint(
    lint_null_constraint: core.Linter,
) -> None:
    """Test fail noqa null constraint."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE tbl (age int NULL);
    """

    violations: core.ViolationMetric = lint_null_constraint.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_null_constraint(
    lint_null_constraint: core.Linter,
    null_constraint: core.BaseChecker,
) -> None:
    """Test fail fix null constraint."""
    sql_fail: str = "CREATE TABLE tbl (age int NULL)"

    sql_fix: str = "CREATE TABLE tbl (\n    age integer\n);"

    null_constraint.config.lint.fix = True

    violations: core.ViolationMetric = lint_null_constraint.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_null_constraint(
    lint_null_constraint: core.Linter,
    null_constraint: core.BaseChecker,
) -> None:
    """Test fail fix null constraint."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN age int NULL;"

    sql_fix: str = "ALTER TABLE tbl\n    ADD COLUMN age integer;"

    null_constraint.config.lint.fix = True

    violations: core.ViolationMetric = lint_null_constraint.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
