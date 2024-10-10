"""Test invalid unique key name."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.naming.NM003 import InvalidUniqueKeyName


@pytest.fixture(scope="module")
def invalid_unique_key_name() -> core.BaseChecker:
    """Create an instance of invalid unique key name."""
    core.add_set_locations_to_rule(InvalidUniqueKeyName)
    return InvalidUniqueKeyName()


@pytest.fixture
def lint_invalid_unique_key_name(
    linter: core.Linter,
    invalid_unique_key_name: core.BaseChecker,
) -> core.Linter:
    """Lint invalid unique key name."""
    invalid_unique_key_name.config.lint.regex_constraint_unique_key = (
        "[a-zA-Z0-9]+_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_key$"
    )

    linter.checkers.add(invalid_unique_key_name)

    return linter


def test_invalid_unique_key_name_rule_code(
    invalid_unique_key_name: core.BaseChecker,
) -> None:
    """Test invalid unique key name rule code."""
    assert (
        invalid_unique_key_name.code == invalid_unique_key_name.__module__.split(".")[-1]
    )


def test_invalid_unique_key_name_auto_fixable(
    invalid_unique_key_name: core.BaseChecker,
) -> None:
    """Test invalid unique key name auto fixable."""
    assert invalid_unique_key_name.is_auto_fixable is False


def test_pass_implicit_unique_key_name_create_table(
    lint_invalid_unique_key_name: core.Linter,
) -> None:
    """Test pass implicit unique key name."""
    sql_fail: str = "CREATE TABLE tbl (tbl_id bigint UNIQUE);"

    violations: core.ViolationMetric = lint_invalid_unique_key_name.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_implicit_unique_key_name_alter_table(
    lint_invalid_unique_key_name: core.Linter,
) -> None:
    """Test pass implicit unique key name."""
    sql_fail: str = "ALTER TABLE tbl ADD UNIQUE (tbl_id);"

    violations: core.ViolationMetric = lint_invalid_unique_key_name.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_valid_unique_key_name(
    lint_invalid_unique_key_name: core.Linter,
) -> None:
    """Test pass valid unique key name."""
    sql_pass: str = """
    CREATE TABLE tbl (tbl_id bigint, CONSTRAINT tbl_tbl_id_key UNIQUE (tbl_id));
    """

    violations: core.ViolationMetric = lint_invalid_unique_key_name.run(
        file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_invalid_unique_key_name(
    lint_invalid_unique_key_name: core.Linter,
) -> None:
    """Test fail invalid unique key name."""
    sql_fail: str = """
    ALTER TABLE tbl ADD CONSTRAINT tbl_key UNIQUE (tbl_id);
    """

    violations: core.ViolationMetric = lint_invalid_unique_key_name.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_invalid_unique_key_name_description(
    lint_invalid_unique_key_name: core.Linter,
    invalid_unique_key_name: core.BaseChecker,
) -> None:
    """Test invalid unique key name description."""
    sql_fail: str = """
    CREATE TABLE tbl (tbl_id bigint, CONSTRAINT tbl_key UNIQUE (tbl_id));
    """

    _: core.ViolationMetric = lint_invalid_unique_key_name.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(invalid_unique_key_name.violations),
        ).description
        == f"Unique key constraint `tbl_key` does not follow naming convention `{invalid_unique_key_name.config.lint.regex_constraint_unique_key}`"  # noqa: E501
    )


def test_pass_noqa_invalid_unique_key_name(
    lint_invalid_unique_key_name: core.Linter,
) -> None:
    """Test pass noqa invalid unique key name."""
    sql_pass_noqa: str = """
    -- noqa: NM003
    ALTER TABLE tbl ADD CONSTRAINT tbl_key UNIQUE (tbl_id);
    """

    violations: core.ViolationMetric = lint_invalid_unique_key_name.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_invalid_unique_key_name(
    lint_invalid_unique_key_name: core.Linter,
) -> None:
    """Test fail noqa invalid unique key name."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE tbl (tbl_id bigint, CONSTRAINT key_tbl UNIQUE (tbl_id));
    """

    violations: core.ViolationMetric = lint_invalid_unique_key_name.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_invalid_unique_key_name(
    lint_invalid_unique_key_name: core.Linter,
) -> None:
    """Test pass noqa invalid unique key name."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (tbl_id bigint, CONSTRAINT tbl_key UNIQUE (tbl_id));
    """

    violations: core.ViolationMetric = lint_invalid_unique_key_name.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
