"""Test for nullable required column."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.core import config
from pgrubic.rules.general.GN013 import NullableRequiredColumn


@pytest.fixture(scope="module")
def nullable_required_column() -> core.BaseChecker:
    """Create an instance of NullableRequiredColumn."""
    core.add_apply_fix_to_rule(NullableRequiredColumn)
    core.add_set_locations_to_rule(NullableRequiredColumn)
    return NullableRequiredColumn()


@pytest.fixture
def lint_nullable_required_column(
    linter: core.Linter,
    nullable_required_column: core.BaseChecker,
) -> core.Linter:
    """Lint NullableRequiredColumn."""
    nullable_required_column.config.lint.fix = False
    nullable_required_column.config.lint.required_columns = [
        config.Column(
            name="created_at",
            data_type="timestamptz",
        ),
    ]
    linter.checkers.add(nullable_required_column)

    return linter


def test_nullable_required_column_rule_code(
    nullable_required_column: core.BaseChecker,
) -> None:
    """Test nullable required column rule code."""
    assert (
        nullable_required_column.code
        == nullable_required_column.__module__.split(".")[-1]
    )


def test_nullable_required_column_auto_fixable(
    nullable_required_column: core.BaseChecker,
) -> None:
    """Test nullable required column auto fixable."""
    assert nullable_required_column.is_auto_fixable is True


def test_pass_no_columns_table(
    lint_nullable_required_column: core.Linter,
) -> None:
    """Test fail nullable required column."""
    sql_fail: str = "CREATE TABLE music ();"

    violations: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_not_nullable_required_column(
    lint_nullable_required_column: core.Linter,
) -> None:
    """Test fail nullable required column."""
    sql_fail: str = "CREATE TABLE music (age int, created_at timestamptz NOT NULL);"

    violations: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_nullable_required_column(
    lint_nullable_required_column: core.Linter,
) -> None:
    """Test fail nullable required column."""
    sql_fail: str = "CREATE TABLE music (age int, created_at timestamptz);"

    violations: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_nullable_required_column(
    lint_nullable_required_column: core.Linter,
) -> None:
    """Test fail nullable required column."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timestamptz;"

    violations: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_nullable_required_column_description(
    lint_nullable_required_column: core.Linter,
    nullable_required_column: core.BaseChecker,
) -> None:
    """Test nullable required column description."""
    sql_fail: str = "CREATE TABLE music (age int, created_at timestamptz);"

    _: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(nullable_required_column.violations),
        ).description
        == "Column `created_at` is marked as required in config"
    )


def test_pass_noqa_nullable_required_column(
    lint_nullable_required_column: core.Linter,
) -> None:
    """Test pass noqa nullable required column."""
    sql_pass_noqa: str = """
    -- noqa: GN013
    CREATE TABLE music (age int, created_at timestamptz)
    """

    violations: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_nullable_required_column(
    lint_nullable_required_column: core.Linter,
) -> None:
    """Test fail noqa nullable required column."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE music (age int, created_at timestamptz);
    """

    violations: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_nullable_required_column(
    lint_nullable_required_column: core.Linter,
) -> None:
    """Test fail noqa nullable required column."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE music (age int)
    """

    violations: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_nullable_required_column(
    lint_nullable_required_column: core.Linter,
    nullable_required_column: core.BaseChecker,
) -> None:
    """Test fail fix nullable required column."""
    sql_fail: str = "CREATE TABLE music (age int, created_at timestamptz);"

    sql_fix: str = (
        "CREATE TABLE music (\n    age integer\n  , created_at timestamptz NOT NULL\n);"
    )

    nullable_required_column.config.lint.fix = True

    violations: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_nullable_required_column(
    lint_nullable_required_column: core.Linter,
    nullable_required_column: core.BaseChecker,
) -> None:
    """Test fail fix nullable required column."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN created_at timestamptz;"

    sql_fix: str = "ALTER TABLE music\n    ADD COLUMN created_at timestamptz NOT NULL;"

    nullable_required_column.config.lint.fix = True

    violations: core.ViolationMetric = lint_nullable_required_column.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
