"""Test wrongly typed required column."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.core import config
from pgrubic.rules.general.GN028 import WronglyTypedRequiredColumn


@pytest.fixture(scope="module")
def wrongly_typed_required_column() -> core.BaseChecker:
    """Create an instance of WronglyTypedRequiredColumn."""
    core.add_apply_fix_to_rule(WronglyTypedRequiredColumn)
    core.add_set_locations_to_rule(WronglyTypedRequiredColumn)
    return WronglyTypedRequiredColumn()


@pytest.fixture
def lint_wrongly_typed_required_column(
    linter: core.Linter,
    wrongly_typed_required_column: core.BaseChecker,
) -> core.Linter:
    """Lint WronglyTypedRequiredColumn."""
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


def test_pass_no_columns_table(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test pass wrongly typed required column."""
    sql_fail: str = "CREATE TABLE music ();"

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


def test_pass_add_columns_table(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test pass add column."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN age int;"

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


def test_pass_not_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test fail wrongly typed required column."""
    sql_fail: str = "CREATE TABLE music (age int, created_at timestamptz);"

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
    sql_fail: str = "CREATE TABLE music (age int, created_at date);"

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
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at date;"

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
    sql_fail: str = "CREATE TABLE music (age int, created_at date);"

    _: core.ViolationMetric = lint_wrongly_typed_required_column.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(wrongly_typed_required_column.violations),
        ).description
        == "Wrongly typed required column `created_at`, expected type is `timestamptz`"
    )


def test_pass_noqa_wrongly_typed_required_column(
    lint_wrongly_typed_required_column: core.Linter,
) -> None:
    """Test pass noqa wrongly typed required column."""
    sql_pass_noqa: str = """
    -- noqa: GN013
    CREATE TABLE music (age int, created_at timestamptz)
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
    CREATE TABLE music (age int, created_at date);
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
    """Test fail noqa wrongly typed required column."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE music (age int, created_at date)
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
    sql_fail: str = "CREATE TABLE music (age int, created_at date);"

    sql_fix: str = (
        "CREATE TABLE music (\n    age integer\n  , created_at timestamptz NOT NULL\n);"
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
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at date;"

    sql_fix: str = "ALTER TABLE music\n    ADD COLUMN created_at timestamptz NOT NULL;"

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
