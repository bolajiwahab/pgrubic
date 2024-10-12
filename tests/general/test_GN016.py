"""Test constant generated column."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN016 import ConstantGeneratedColumn


@pytest.fixture(scope="module")
def constant_generated_column() -> core.BaseChecker:
    """Create an instance of ConstantGeneratedColumn."""
    core.add_set_locations_to_rule(ConstantGeneratedColumn)
    return ConstantGeneratedColumn()


@pytest.fixture
def lint_constant_generated_column(
    linter: core.Linter,
    constant_generated_column: core.BaseChecker,
) -> core.Linter:
    """Lint ConstantGeneratedColumn."""
    linter.checkers.add(constant_generated_column)

    return linter


def test_constant_generated_column_rule_code(
    constant_generated_column: core.BaseChecker,
) -> None:
    """Test constant generated column rule code."""
    assert (
        constant_generated_column.code
        == constant_generated_column.__module__.split(".")[-1]
    )


def test_constant_generated_column_auto_fixable(
    constant_generated_column: core.BaseChecker,
) -> None:
    """Test constant generated column auto fixable."""
    assert constant_generated_column.is_auto_fixable is False


def test_pass_create_table_generated_column(
    lint_constant_generated_column: core.Linter,
) -> None:
    """Test pass create table generated column."""
    sql_pass: str = """
    CREATE TABLE people (
        height_cm numeric,
        height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED
    );
    """

    violations: core.ViolationMetric = lint_constant_generated_column.run(
        file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_generated_column(
    lint_constant_generated_column: core.Linter,
) -> None:
    """Test pass alter table generated column."""
    sql_fail: str = """
    ALTER TABLE people
        ADD COLUMN height_in numeric GENERATED ALWAYS AS (height_cm / 2.54) STORED;
    """

    violations: core.ViolationMetric = lint_constant_generated_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_constant_generated_column(
    lint_constant_generated_column: core.Linter,
) -> None:
    """Test fail constant generated column."""
    sql_fail: str = """
    CREATE TABLE people (
        height_in numeric GENERATED ALWAYS AS (2.54) STORED
    );
    """

    violations: core.ViolationMetric = lint_constant_generated_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_constant_generated_column_description(
    lint_constant_generated_column: core.Linter,
    constant_generated_column: core.BaseChecker,
) -> None:
    """Test constant generated column description."""
    sql_fail: str = """
    ALTER TABLE people
        ADD COLUMN height_in numeric GENERATED ALWAYS AS (2.54) STORED;
    """

    _: core.ViolationMetric = lint_constant_generated_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(constant_generated_column.violations),
        ).description
        == "Generated column `height_in` should not be a constant"
    )


def test_pass_noqa_constant_generated_column(
    lint_constant_generated_column: core.Linter,
) -> None:
    """Test pass noqa constant generated column."""
    sql_pass_noqa: str = """
    -- noqa: GN016
    ALTER TABLE people
        ADD COLUMN height_in numeric GENERATED ALWAYS AS (2.54) STORED;
    """

    violations: core.ViolationMetric = lint_constant_generated_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_constant_generated_column(
    lint_constant_generated_column: core.Linter,
) -> None:
    """Test fail noqa constant generated column."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE people
        ADD COLUMN height_in numeric GENERATED ALWAYS AS (2.54) STORED;
    """

    violations: core.ViolationMetric = lint_constant_generated_column.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_constant_generated_column(
    lint_constant_generated_column: core.Linter,
) -> None:
    """Test fail noqa constant generated column."""
    sql_pass_noqa: str = """
    -- noqa
    ALTER TABLE people
        ADD COLUMN height_in numeric GENERATED ALWAYS AS (2.54) STORED;
    """

    violations: core.ViolationMetric = lint_constant_generated_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
