"""Test usage of wrongly typed required column."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.core import config
from pgrubic.rules.typing.TP015 import WronglyTypedRequiredColumn


@pytest.fixture(scope="module")
def wrongly_typed_required_column() -> core.BaseChecker:
    """Create an instance of wrongly typed required column."""
    core.add_apply_fix_to_rule(WronglyTypedRequiredColumn)
    core.add_set_locations_to_rule(WronglyTypedRequiredColumn)
    return WronglyTypedRequiredColumn()


@pytest.fixture
def lint_wrongly_typed_required_column(
    linter: core.Linter,
    wrongly_typed_required_column: core.BaseChecker,
) -> core.Linter:
    """Lint wrongly typed required column."""
    wrongly_typed_required_column.config.lint.fix = False
    wrongly_typed_required_column.config.lint.required_columns = [
        config.Column(
            name="created_at",
            data_type="timestamptz",
        ),
    ]
    linter.checkers.add(wrongly_typed_required_column)

    return linter


def test_wrongly_typed_required_column_rule_code(
    wrongly_typed_required_column: core.BaseChecker,
) -> None:
    """Test wrongly typed required column rule code."""
    assert (
        wrongly_typed_required_column.code
        == wrongly_typed_required_column.__module__.split(".")[-1]
    )


def test_wrongly_typed_required_column_auto_fixable(
    wrongly_typed_required_column: core.BaseChecker,
) -> None:
    """Test wrongly typed required column auto fixable."""
    assert wrongly_typed_required_column.is_auto_fixable is True


def test_pass_create_table_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test pass correctly typed required column."""
    sql_fail: str = "CREATE TABLE tbl (created_at timestamptz);"

    violations: core.ViolationMetric = lint_wrongly_typed_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_wrongly_typed_required_columnb(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test pass correctly typed required column."""
    sql_fail: str = """
    ALTER TABLE tbl ADD COLUMN created_at timestamptz;
    """

    violations: core.ViolationMetric = lint_wrongly_typed_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test fail create table wrongly typed required column."""
    sql_fail: str = "CREATE TABLE tbl (created_at timestamp);"

    violations: core.ViolationMetric = lint_wrongly_typed_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test fail alter table wrongly typed required column."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN created_at text;"

    violations: core.ViolationMetric = lint_wrongly_typed_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_wrongly_typed_required_column_description(
    lint_wrongly_typed_required_column: core.Linter,
    wrongly_typed_required_column: core.BaseChecker,
) -> None:
    """Test wrongly typed required column description."""
    sql_fail: str = "CREATE TABLE tbl (created_at varchar);"

    _: core.ViolationMetric = lint_wrongly_typed_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(wrongly_typed_required_column.violations),
        ).description
        == "Column 'created_at' expected type is 'timestamptz', found 'varchar'"
    )


def test_pass_noqa_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test pass noqa wrongly typed required column."""
    sql_pass_noqa: str = """
    -- noqa: TP015
    CREATE TABLE tbl (tbl_id int, created_at varchar)
    """

    violations: core.ViolationMetric = lint_wrongly_typed_required_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test fail noqa wrongly typed required column."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN created_at bigint;
    """

    violations: core.ViolationMetric = lint_wrongly_typed_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test pass noqa wrongly typed required column."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (tbl_id int, created_at text);
    """

    violations: core.ViolationMetric = lint_wrongly_typed_required_column.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
    wrongly_typed_required_column: core.BaseChecker,
) -> None:
    """Test fail fix wrongly typed required column."""
    sql_fail: str = "CREATE TABLE tbl (user_id int, created_at varchar);"

    sql_fix: str = (
        "CREATE TABLE tbl (\n    user_id integer\n  , created_at timestamptz\n);"
    )

    wrongly_typed_required_column.config.lint.fix = True

    violations: core.ViolationMetric = lint_wrongly_typed_required_column.run(
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


def test_fail_fix_alter_table_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
    wrongly_typed_required_column: core.BaseChecker,
) -> None:
    """Test fail fix wrongly typed required column."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN created_at varchar;"

    sql_fix: str = "ALTER TABLE tbl\n    ADD COLUMN created_at timestamptz;"

    wrongly_typed_required_column.config.lint.fix = True

    violations: core.ViolationMetric = lint_wrongly_typed_required_column.run(
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
