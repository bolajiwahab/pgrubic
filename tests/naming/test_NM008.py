"""Test implicit constraint name."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.naming.NM008 import ImplicitConstraintName


@pytest.fixture(scope="module")
def implicit_constraint_name() -> core.BaseChecker:
    """Create an instance of implicit constraint name."""
    core.add_set_locations_to_rule(ImplicitConstraintName)
    return ImplicitConstraintName()


@pytest.fixture
def lint_implicit_constraint_name(
    linter: core.Linter,
    implicit_constraint_name: core.BaseChecker,
) -> core.Linter:
    """Lint implicit constraint name."""
    linter.checkers.add(implicit_constraint_name)

    return linter


def test_implicit_constraint_name_rule_code(
    implicit_constraint_name: core.BaseChecker,
) -> None:
    """Test implicit constraint name rule code."""
    assert (
        implicit_constraint_name.code
        == implicit_constraint_name.__module__.split(".")[-1]
    )


def test_implicit_constraint_name_auto_fixable(
    implicit_constraint_name: core.BaseChecker,
) -> None:
    """Test implicit constraint name auto fixable."""
    assert implicit_constraint_name.is_auto_fixable is False


def test_pass_explicit_constraint_name_create_table(
    lint_implicit_constraint_name: core.Linter,
) -> None:
    """Test pass explicit constraint name."""
    sql_pass: str = "CREATE TABLE tbl (col int, CONSTRAINT tbl_pkey PRIMARY KEY (col));"

    violations: core.ViolationMetric = lint_implicit_constraint_name.run(
        file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_explicit_constraint_name_add_column(
    lint_implicit_constraint_name: core.Linter,
) -> None:
    """Test pass explicit constraint name."""
    sql_fail: str = "ALTER TABLE tbl ADD CONSTRAINT tbl_pkey PRIMARY KEY (col);"

    violations: core.ViolationMetric = lint_implicit_constraint_name.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_implicit_constraint_name(
    lint_implicit_constraint_name: core.Linter,
) -> None:
    """Test fail implicit constraint name."""
    sql_fail: str = "CREATE TABLE tbl (col int PRIMARY KEY)"

    violations: core.ViolationMetric = lint_implicit_constraint_name.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_implicit_constraint_name_description(
    lint_implicit_constraint_name: core.Linter,
    implicit_constraint_name: core.BaseChecker,
) -> None:
    """Test implicit constraint name description."""
    sql_fail: str = "ALTER TABLE tbl ADD PRIMARY KEY (col);"

    _: core.ViolationMetric = lint_implicit_constraint_name.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(implicit_constraint_name.violations),
        ).description
        == "Prefer named constraint"
    )


def test_pass_noqa_implicit_constraint_name(
    lint_implicit_constraint_name: core.Linter,
) -> None:
    """Test pass noqa implicit constraint name."""
    sql_pass_noqa: str = """
    -- noqa: NM008
    ALTER TABLE tbl ADD PRIMARY KEY (col);
    """

    violations: core.ViolationMetric = lint_implicit_constraint_name.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_implicit_constraint_name(
    lint_implicit_constraint_name: core.Linter,
) -> None:
    """Test fail noqa implicit constraint name."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE tbl (col int PRIMARY KEY)
    """

    violations: core.ViolationMetric = lint_implicit_constraint_name.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_implicit_constraint_name(
    lint_implicit_constraint_name: core.Linter,
) -> None:
    """Test pass noqa implicit constraint name."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE tbl (col int PRIMARY KEY)
    """

    violations: core.ViolationMetric = lint_implicit_constraint_name.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
