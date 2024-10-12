"""Test unlogged table."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN019 import UnloggedTable


@pytest.fixture(scope="module")
def unlogged_table() -> core.BaseChecker:
    """Create an instance of UnloggedTable."""
    core.add_apply_fix_to_rule(UnloggedTable)
    core.add_set_locations_to_rule(UnloggedTable)
    return UnloggedTable()


@pytest.fixture
def lint_unlogged_table(
    linter: core.Linter,
    unlogged_table: core.BaseChecker,
) -> core.Linter:
    """Lint UnloggedTable."""
    unlogged_table.config.lint.fix = False
    linter.checkers.add(unlogged_table)

    return linter


def test_unlogged_table_rule_code(
    unlogged_table: core.BaseChecker,
) -> None:
    """Test unlogged table rule code."""
    assert unlogged_table.code == unlogged_table.__module__.split(".")[-1]


def test_unlogged_table_auto_fixable(
    unlogged_table: core.BaseChecker,
) -> None:
    """Test unlogged table auto fixable."""
    assert unlogged_table.is_auto_fixable is True


def test_fail_unlogged_table(
    lint_unlogged_table: core.Linter,
) -> None:
    """Test fail unlogged table."""
    sql_fail: str = "CREATE UNLOGGED TABLE tbl (id int);"

    violations: core.ViolationMetric = lint_unlogged_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_unlogged_table_description(
    lint_unlogged_table: core.Linter,
    unlogged_table: core.BaseChecker,
) -> None:
    """Test unlogged table description."""
    sql_fail: str = "ALTER TABLE tbl SET UNLOGGED;"

    _: core.ViolationMetric = lint_unlogged_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(unlogged_table.violations),
        ).description
        == "Prefer regular table to unlogged table"
    )


def test_pass_noqa_unlogged_table(
    lint_unlogged_table: core.Linter,
) -> None:
    """Test pass noqa unlogged table."""
    sql_pass_noqa: str = """
    -- noqa: GN019
    CREATE UNLOGGED TABLE tbl (id int);
    """

    violations: core.ViolationMetric = lint_unlogged_table.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_unlogged_table(
    lint_unlogged_table: core.Linter,
) -> None:
    """Test fail noqa unlogged table."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl SET UNLOGGED;
    """

    violations: core.ViolationMetric = lint_unlogged_table.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_unlogged_table(
    lint_unlogged_table: core.Linter,
) -> None:
    """Test fail noqa unlogged table."""
    sql_pass_noqa: str = """
    -- noqa
    ALTER TABLE tbl SET UNLOGGED;
    """

    violations: core.ViolationMetric = lint_unlogged_table.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_unlogged_table(
    lint_unlogged_table: core.Linter,
    unlogged_table: core.BaseChecker,
) -> None:
    """Test fail fix unlogged table."""
    sql_fail: str = "CREATE UNLOGGED TABLE account (id int);"

    sql_fix: str = "CREATE TABLE account (\n    id integer\n);"

    unlogged_table.config.lint.fix = True

    violations: core.ViolationMetric = lint_unlogged_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_unlogged_table(
    lint_unlogged_table: core.Linter,
    unlogged_table: core.BaseChecker,
) -> None:
    """Test fail fix unlogged table."""
    sql_fail: str = "ALTER TABLE account SET UNLOGGED;"

    sql_fix: str = "ALTER TABLE account\n    SET LOGGED;"

    unlogged_table.config.lint.fix = True

    violations: core.ViolationMetric = lint_unlogged_table.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
