"""Test table column conflict."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN010 import TableColumnConflict


@pytest.fixture(scope="module")
def table_column_conflict() -> core.BaseChecker:
    """Create an instance of TableColumnConflict."""
    core.add_set_locations_to_rule(TableColumnConflict)
    return TableColumnConflict()


@pytest.fixture
def lint_table_column_conflict(
    linter: core.Linter,
    table_column_conflict: core.BaseChecker,
) -> core.Linter:
    """Lint TableColumnConflict."""
    linter.checkers.add(table_column_conflict)

    return linter


def test_table_column_conflict_rule_code(
    table_column_conflict: core.BaseChecker,
) -> None:
    """Test table column conflict rule code."""
    assert table_column_conflict.code == table_column_conflict.__module__.split(".")[-1]


def test_table_column_conflict_auto_fixable(
    table_column_conflict: core.BaseChecker,
) -> None:
    """Test table column conflict auto fixable."""
    assert table_column_conflict.is_auto_fixable is False


def test_pass_no_table_column_conflict(
    lint_table_column_conflict: core.Linter,
) -> None:
    """Test fail table column conflict."""
    sql_fail: str = "CREATE TABLE music (age int, age text);"

    violations: core.ViolationMetric = lint_table_column_conflict.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_table_column_conflict(
    lint_table_column_conflict: core.Linter,
) -> None:
    """Test fail table column conflict."""
    sql_fail: str = "CREATE TABLE music (age int, music text);"

    violations: core.ViolationMetric = lint_table_column_conflict.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_table_column_conflict_description(
    lint_table_column_conflict: core.Linter,
    table_column_conflict: core.BaseChecker,
) -> None:
    """Test table column conflict description."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN music text;"

    _: core.ViolationMetric = lint_table_column_conflict.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(table_column_conflict.violations),
        ).description
        == "Table name `music` conflicts with the name of its column(s)"
    )


def test_pass_noqa_table_column_conflict(
    lint_table_column_conflict: core.Linter,
) -> None:
    """Test pass noqa table column conflict."""
    sql_pass_noqa: str = """
    -- noqa: GN010
    CREATE TABLE music (age int, music text);
    """

    violations: core.ViolationMetric = lint_table_column_conflict.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_table_column_conflict(
    lint_table_column_conflict: core.Linter,
) -> None:
    """Test fail noqa table column conflict."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE music (age int, music text);
    """

    violations: core.ViolationMetric = lint_table_column_conflict.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_table_column_conflict(
    lint_table_column_conflict: core.Linter,
) -> None:
    """Test fail noqa table column conflict."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE music (age int, music text);
    """

    violations: core.ViolationMetric = lint_table_column_conflict.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
