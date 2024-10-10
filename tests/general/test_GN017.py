"""Test id column."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN017 import IdColumn


@pytest.fixture(scope="module")
def id_column() -> core.BaseChecker:
    """Create an instance of IdColumn."""
    core.add_apply_fix_to_rule(IdColumn)
    core.add_set_locations_to_rule(IdColumn)
    return IdColumn()


@pytest.fixture
def lint_id_column(
    linter: core.Linter,
    id_column: core.BaseChecker,
) -> core.Linter:
    """Lint IdColumn."""
    id_column.config.lint.fix = False
    linter.checkers.add(id_column)

    return linter


def test_id_column_rule_code(
    id_column: core.BaseChecker,
) -> None:
    """Test id column rule code."""
    assert id_column.code == id_column.__module__.split(".")[-1]


def test_id_column_auto_fixable(
    id_column: core.BaseChecker,
) -> None:
    """Test id column auto fixable."""
    assert id_column.is_auto_fixable is True


def test_fail_id_column(
    lint_id_column: core.Linter,
) -> None:
    """Test fail id column."""
    sql_fail: str = "CREATE TABLE tbl (id int);"

    violations: core.ViolationMetric = lint_id_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_id_column_description(
    lint_id_column: core.Linter,
    id_column: core.BaseChecker,
) -> None:
    """Test id column description."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN id int;"

    _: core.ViolationMetric = lint_id_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(id_column.violations),
        ).description
        == "Use descriptive name for column instead of `id`"
    )


def test_pass_noqa_id_column(
    lint_id_column: core.Linter,
) -> None:
    """Test pass noqa id column."""
    sql_pass_noqa: str = """
    -- noqa: GN017
    CREATE TABLE tbl (id int);
    """

    violations: core.ViolationMetric = lint_id_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_id_column(
    lint_id_column: core.Linter,
) -> None:
    """Test fail noqa id column."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN id int;
    """

    violations: core.ViolationMetric = lint_id_column.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_id_column(
    lint_id_column: core.Linter,
) -> None:
    """Test fail noqa id column."""
    sql_pass_noqa: str = """
    -- noqa:
    ALTER TABLE tbl ADD COLUMN id int;
    """

    violations: core.ViolationMetric = lint_id_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_id_column(
    lint_id_column: core.Linter,
    id_column: core.BaseChecker,
) -> None:
    """Test fail fix id column."""
    sql_fail: str = "CREATE TABLE account (id int);"

    sql_fix: str = "CREATE TABLE account (\n    account_id integer\n);"

    id_column.config.lint.fix = True

    violations: core.ViolationMetric = lint_id_column.run(
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


def test_fail_fix_alter_table_id_column(
    lint_id_column: core.Linter,
    id_column: core.BaseChecker,
) -> None:
    """Test fail fix id column."""
    sql_fail: str = "ALTER TABLE account ADD COLUMN id int;"

    sql_fix: str = "ALTER TABLE account\n    ADD COLUMN account_id integer;"

    id_column.config.lint.fix = True

    violations: core.ViolationMetric = lint_id_column.run(
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
