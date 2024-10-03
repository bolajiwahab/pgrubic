"""Test usage of mismatch column in data type change."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.typing.TP018 import MismatchColumnInDataTypeChange


@pytest.fixture(scope="module")
def mismatch_column_in_data_type_change() -> core.BaseChecker:
    """Create an instance of mismatch column in data type change."""
    core.add_apply_fix_to_rule(MismatchColumnInDataTypeChange)
    core.add_set_locations_to_rule(MismatchColumnInDataTypeChange)
    return MismatchColumnInDataTypeChange()


@pytest.fixture
def lint_mismatch_column_in_data_type_change(
    linter: core.Linter,
    mismatch_column_in_data_type_change: core.BaseChecker,
) -> core.Linter:
    """Lint mismatch column in data type change."""
    linter.checkers.add(mismatch_column_in_data_type_change)

    return linter


def test_mismatch_column_in_data_type_change_rule_code(
    mismatch_column_in_data_type_change: core.BaseChecker,
) -> None:
    """Test mismatch column in data type change rule code."""
    assert (
        mismatch_column_in_data_type_change.code
        == mismatch_column_in_data_type_change.__module__.split(".")[-1]
    )


def test_mismatch_column_in_data_type_change_auto_fixable(
    mismatch_column_in_data_type_change: core.BaseChecker,
) -> None:
    """Test mismatch column in data type change auto fixable."""
    assert mismatch_column_in_data_type_change.is_auto_fixable is False


def test_pass_match_column_in_data_type_change(
    lint_mismatch_column_in_data_type_change: core.Linter,
) -> None:
    """Test pass match column in data type change."""
    sql_fail: str = """
    ALTER TABLE account ALTER COLUMN user_id TYPE uuid USING user_id::uuid;
    """

    violations: core.ViolationMetric = lint_mismatch_column_in_data_type_change.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_mismatch_column_in_data_type_change(
    lint_mismatch_column_in_data_type_change: core.Linter,
) -> None:
    """Test fail alter table mismatch column in data type change."""
    sql_fail: str = """
    ALTER TABLE account ALTER COLUMN user_id TYPE uuid USING account_id::uuid;
    """

    violations: core.ViolationMetric = lint_mismatch_column_in_data_type_change.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_mismatch_column_in_data_type_change_description(
    lint_mismatch_column_in_data_type_change: core.Linter,
    mismatch_column_in_data_type_change: core.BaseChecker,
) -> None:
    """Test mismatch column in data type change description."""
    sql_fail: str = """
    ALTER TABLE account ALTER COLUMN user_id TYPE uuid USING account_id::uuid;
    """

    _: core.ViolationMetric = lint_mismatch_column_in_data_type_change.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(mismatch_column_in_data_type_change.violations),
        ).description
        == "Column `user_id` in data type change does not match column `account_id` in USING clause"  # noqa: E501
    )


def test_pass_noqa_mismatch_column_in_data_type_change(
    lint_mismatch_column_in_data_type_change: core.Linter,
) -> None:
    """Test pass noqa mismatch column in data type change."""
    sql_pass_noqa: str = """
    -- noqa: TP018
    ALTER TABLE account ALTER COLUMN user_id TYPE uuid USING account_id::uuid;
    """

    violations: core.ViolationMetric = lint_mismatch_column_in_data_type_change.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_mismatch_column_in_data_type_change(
    lint_mismatch_column_in_data_type_change: core.Linter,
) -> None:
    """Test fail noqa mismatch column in data type change."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE account ALTER COLUMN user_id TYPE uuid USING account_id::uuid;
    """

    violations: core.ViolationMetric = lint_mismatch_column_in_data_type_change.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_mismatch_column_in_data_type_change(
    lint_mismatch_column_in_data_type_change: core.Linter,
) -> None:
    """Test pass noqa mismatch column in data type change."""
    sql_pass_noqa: str = """
    -- noqa:
    ALTER TABLE account ALTER COLUMN user_id TYPE uuid USING account_id::uuid;
    """

    violations: core.ViolationMetric = lint_mismatch_column_in_data_type_change.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
