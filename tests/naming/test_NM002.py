"""Test invalid primary key name."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.naming.NM002 import InvalidPrimaryKeyName


@pytest.fixture(scope="module")
def invalid_primary_key_name() -> core.BaseChecker:
    """Create an instance of invalid primary key name."""
    core.add_set_locations_to_rule(InvalidPrimaryKeyName)
    return InvalidPrimaryKeyName()


@pytest.fixture
def lint_invalid_primary_key_name(
    linter: core.Linter,
    invalid_primary_key_name: core.BaseChecker,
) -> core.Linter:
    """Lint invalid primary key name."""
    invalid_primary_key_name.config.lint.regex_constraint_primary_key = (
        "[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_pkey$"
    )

    linter.checkers.add(invalid_primary_key_name)

    return linter


def test_invalid_primary_key_name_rule_code(
    invalid_primary_key_name: core.BaseChecker,
) -> None:
    """Test invalid primary key name rule code."""
    assert (
        invalid_primary_key_name.code
        == invalid_primary_key_name.__module__.split(".")[-1]
    )


def test_invalid_primary_key_name_auto_fixable(
    invalid_primary_key_name: core.BaseChecker,
) -> None:
    """Test invalid primary key name auto fixable."""
    assert invalid_primary_key_name.is_auto_fixable is False


def test_pass_implicit_primary_key_name_create_table(
    lint_invalid_primary_key_name: core.Linter,
) -> None:
    """Test pass implicit primary key name."""
    sql_fail: str = "CREATE TABLE tbl (tbl_id bigint PRIMARY KEY);"

    violations: core.ViolationMetric = lint_invalid_primary_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_implicit_primary_key_name_alter_table(
    lint_invalid_primary_key_name: core.Linter,
) -> None:
    """Test pass implicit primary key name."""
    sql_fail: str = "ALTER TABLE tbl ADD PRIMARY KEY (tbl_id);"

    violations: core.ViolationMetric = lint_invalid_primary_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_valid_primary_key_name(
    lint_invalid_primary_key_name: core.Linter,
) -> None:
    """Test pass valid primary key name."""
    sql_pass: str = """
    CREATE TABLE tbl (tbl_id bigint, CONSTRAINT tbl_pkey PRIMARY KEY (tbl_id));
    """

    violations: core.ViolationMetric = lint_invalid_primary_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_invalid_primary_key_name(
    lint_invalid_primary_key_name: core.Linter,
) -> None:
    """Test fail invalid primary key name."""
    sql_fail: str = """
    ALTER TABLE tbl ADD CONSTRAINT pkey PRIMARY KEY (tbl_id);
    """

    violations: core.ViolationMetric = lint_invalid_primary_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_invalid_primary_key_name_description(
    lint_invalid_primary_key_name: core.Linter,
    invalid_primary_key_name: core.BaseChecker,
) -> None:
    """Test invalid primary key name description."""
    sql_fail: str = """
    CREATE TABLE tbl (tbl_id bigint, CONSTRAINT pkey_tbl PRIMARY KEY (tbl_id));
    """

    _: core.ViolationMetric = lint_invalid_primary_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(invalid_primary_key_name.violations),
        ).description
        == f"Primary key constraint `pkey_tbl` does not follow naming convention `{invalid_primary_key_name.config.lint.regex_constraint_primary_key}`"  # noqa: E501
    )


def test_pass_noqa_invalid_primary_key_name(
    lint_invalid_primary_key_name: core.Linter,
) -> None:
    """Test pass noqa invalid primary key name."""
    sql_pass_noqa: str = """
    -- noqa: NM002
    ALTER TABLE tbl ADD CONSTRAINT pkey PRIMARY KEY (tbl_id);
    """

    violations: core.ViolationMetric = lint_invalid_primary_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_invalid_primary_key_name(
    lint_invalid_primary_key_name: core.Linter,
) -> None:
    """Test fail noqa invalid primary key name."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE tbl (tbl_id bigint, CONSTRAINT pkey_tbl PRIMARY KEY (tbl_id));
    """

    violations: core.ViolationMetric = lint_invalid_primary_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_invalid_primary_key_name(
    lint_invalid_primary_key_name: core.Linter,
) -> None:
    """Test pass noqa invalid primary key name."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (tbl_id bigint, CONSTRAINT pkey_tbl PRIMARY KEY (tbl_id));
    """

    violations: core.ViolationMetric = lint_invalid_primary_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
