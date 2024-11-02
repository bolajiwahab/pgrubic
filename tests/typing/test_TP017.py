"""Test usage of nullable boolean field."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.typing.TP017 import NullableBooleanField


@pytest.fixture(scope="module")
def nullable_boolean_field() -> core.BaseChecker:
    """Create an instance of nullable boolean field."""
    core.add_apply_fix_to_rule(NullableBooleanField)
    core.add_set_locations_to_rule(NullableBooleanField)
    return NullableBooleanField()


@pytest.fixture
def lint_nullable_boolean_field(
    linter: core.Linter,
    nullable_boolean_field: core.BaseChecker,
) -> core.Linter:
    """Lint nullable boolean field."""
    nullable_boolean_field.config.lint.fix = False
    linter.checkers.add(nullable_boolean_field)

    return linter


def test_nullable_boolean_field_rule_code(
    nullable_boolean_field: core.BaseChecker,
) -> None:
    """Test nullable boolean field rule code."""
    assert nullable_boolean_field.code == nullable_boolean_field.__module__.split(".")[-1]


def test_nullable_boolean_field_auto_fixable(
    nullable_boolean_field: core.BaseChecker,
) -> None:
    """Test nullable boolean field auto fixable."""
    assert nullable_boolean_field.is_auto_fixable is True


def test_pass_create_tablenullable_boolean_field(
    lint_nullable_boolean_field: core.Linter,
) -> None:
    """Test pass boolean not nullable."""
    sql_fail: str = "CREATE TABLE transaction (amount boolean NOT NULL);"

    violations: core.ViolationMetric = lint_nullable_boolean_field.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_tablenullable_boolean_field(
    lint_nullable_boolean_field: core.Linter,
) -> None:
    """Test pass boolean not nullable."""
    sql_fail: str = "ALTER TABLE transaction ADD COLUMN is_active bool NOT NULL;"

    violations: core.ViolationMetric = lint_nullable_boolean_field.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_nullable_boolean_field(
    lint_nullable_boolean_field: core.Linter,
) -> None:
    """Test fail create table nullable boolean field."""
    sql_fail: str = "CREATE TABLE transaction (is_active boolean);"

    violations: core.ViolationMetric = lint_nullable_boolean_field.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_nullable_boolean_field(
    lint_nullable_boolean_field: core.Linter,
) -> None:
    """Test fail alter table nullable boolean field."""
    sql_fail: str = "ALTER TABLE transaction ADD COLUMN is_active boolean;"

    violations: core.ViolationMetric = lint_nullable_boolean_field.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_nullable_boolean_field_description(
    lint_nullable_boolean_field: core.Linter,
    nullable_boolean_field: core.BaseChecker,
) -> None:
    """Test nullable boolean field description."""
    sql_fail: str = "CREATE TABLE transaction (is_active boolean);"

    _: core.ViolationMetric = lint_nullable_boolean_field.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(nullable_boolean_field.violations),
        ).description
        == "Boolean field should be not be nullable"
    )


def test_pass_noqa_nullable_boolean_field(
    lint_nullable_boolean_field: core.Linter,
) -> None:
    """Test pass noqa nullable boolean field."""
    sql_pass_noqa: str = """
    -- noqa: TP017
    CREATE TABLE transaction (transaction_id int, is_active boolean);
    """

    violations: core.ViolationMetric = lint_nullable_boolean_field.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_nullable_boolean_field(
    lint_nullable_boolean_field: core.Linter,
) -> None:
    """Test fail noqa nullable boolean field."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE transaction ADD COLUMN is_active boolean;
    """

    violations: core.ViolationMetric = lint_nullable_boolean_field.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_nullable_boolean_field(
    lint_nullable_boolean_field: core.Linter,
) -> None:
    """Test pass noqa nullable boolean field."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE transaction (transaction_id int, is_active boolean);
    """

    violations: core.ViolationMetric = lint_nullable_boolean_field.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_nullable_boolean_field(
    lint_nullable_boolean_field: core.Linter,
    nullable_boolean_field: core.BaseChecker,
) -> None:
    """Test fail fix nullable boolean field."""
    sql_fail: str = "CREATE TABLE transaction (user_id int, is_active boolean);"

    sql_fix: str = "CREATE TABLE transaction (\n    user_id integer\n  , is_active boolean NOT NULL\n);\n"  # noqa: E501

    nullable_boolean_field.config.lint.fix = True

    violations: core.ViolationMetric = lint_nullable_boolean_field.run(
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


def test_fail_fix_alter_table_nullable_boolean_field(
    lint_nullable_boolean_field: core.Linter,
    nullable_boolean_field: core.BaseChecker,
) -> None:
    """Test fail fix nullable boolean field."""
    sql_fail: str = "ALTER TABLE transaction ADD COLUMN is_active boolean;"

    sql_fix: str = "ALTER TABLE transaction\n    ADD COLUMN is_active boolean NOT NULL;\n"

    nullable_boolean_field.config.lint.fix = True

    violations: core.ViolationMetric = lint_nullable_boolean_field.run(
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
