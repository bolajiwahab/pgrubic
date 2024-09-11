"""Test for duplicate column."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.general.GN009 import DuplicateColumn


@pytest.fixture(scope="module")
def duplicate_column() -> core.BaseChecker:
    """Create an instance of DuplicateColumn."""
    return DuplicateColumn()


@pytest.fixture
def lint_duplicate_column(
    linter: core.Linter,
    duplicate_column: core.BaseChecker,
) -> core.Linter:
    """Lint DuplicateColumn."""
    duplicate_column.config.lint.fix = False
    linter.checkers.add(duplicate_column)

    return linter


def test_duplicate_column_rule_code(
    duplicate_column: core.BaseChecker,
) -> None:
    """Test duplicate column rule code."""
    assert duplicate_column.code == duplicate_column.__module__.split(".")[-1]


def test_duplicate_column_auto_fixable(
    duplicate_column: core.BaseChecker,
) -> None:
    """Test duplicate column auto fixable."""
    assert duplicate_column.is_auto_fixable is False


def test_pass_no_duplicate_column(
    lint_duplicate_column: core.Linter,
) -> None:
    """Test fail duplicate column."""
    sql_fail: str = "CREATE TABLE music (age int, name text);"

    violations: core.ViolationMetric = lint_duplicate_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_duplicate_column(
    lint_duplicate_column: core.Linter,
) -> None:
    """Test fail duplicate column."""
    sql_fail: str = "CREATE TABLE music (age int, age text);"

    violations: core.ViolationMetric = lint_duplicate_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_duplicate_column_description(
    lint_duplicate_column: core.Linter,
    duplicate_column: core.BaseChecker,
) -> None:
    """Test duplicate column description."""
    sql_fail: str = "CREATE TABLE music (age int, age text);"

    _: core.ViolationMetric = lint_duplicate_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(duplicate_column.violations),
        ).description
        == "Column `age` specified more than once"
    )


def test_pass_noqa_duplicate_column(
    lint_duplicate_column: core.Linter,
) -> None:
    """Test pass noqa duplicate column."""
    sql_pass_noqa: str = """
    -- noqa: GN009
    CREATE TABLE music (age int, age text);
    """

    violations: core.ViolationMetric = lint_duplicate_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_duplicate_column(
    lint_duplicate_column: core.Linter,
) -> None:
    """Test fail noqa duplicate column."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE music (age int, age text);
    """

    violations: core.ViolationMetric = lint_duplicate_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_duplicate_column(
    lint_duplicate_column: core.Linter,
) -> None:
    """Test fail noqa duplicate column."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE music (age int, age text);
    """

    violations: core.ViolationMetric = lint_duplicate_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
