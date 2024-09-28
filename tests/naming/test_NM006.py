"""Test for invalid exclusion constraint name."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.naming.NM006 import InvalidExclusionConstraintName


@pytest.fixture(scope="module")
def invalid_exclusion_constraint_name() -> core.BaseChecker:
    """Create an instance of invalid exclusion constraint name."""
    core.add_set_locations_to_rule(InvalidExclusionConstraintName)
    return InvalidExclusionConstraintName()


@pytest.fixture
def lint_invalid_exclusion_constraint_name(
    linter: core.Linter,
    invalid_exclusion_constraint_name: core.BaseChecker,
) -> core.Linter:
    """Lint invalid exclusion constraint name."""
    invalid_exclusion_constraint_name.config.lint.regex_constraint_exclusion = (
        "[a-zA-Z0-9]+_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_exclusion$"
    )

    linter.checkers.add(invalid_exclusion_constraint_name)

    return linter


def test_invalid_exclusion_constraint_name_rule_code(
    invalid_exclusion_constraint_name: core.BaseChecker,
) -> None:
    """Test invalid exclusion constraint name rule code."""
    assert (
        invalid_exclusion_constraint_name.code
        == invalid_exclusion_constraint_name.__module__.split(".")[-1]
    )


def test_invalid_exclusion_constraint_name_auto_fixable(
    invalid_exclusion_constraint_name: core.BaseChecker,
) -> None:
    """Test invalid exclusion constraint name auto fixable."""
    assert invalid_exclusion_constraint_name.is_auto_fixable is False


def test_pass_implicit_exclusion_constraint_name_create_table(
    lint_invalid_exclusion_constraint_name: core.Linter,
) -> None:
    """Test pass implicit exclusion constraint name."""
    sql_fail: str = """
    CREATE TABLE tbl (tbl_id bigint, EXCLUDE USING gist (tbl_id WITH &&));
    """

    violations: core.ViolationMetric = lint_invalid_exclusion_constraint_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_implicit_exclusion_constraint_name_alter_table(
    lint_invalid_exclusion_constraint_name: core.Linter,
) -> None:
    """Test pass implicit exclusion constraint name."""
    sql_fail: str = "ALTER TABLE tbl ADD EXCLUDE USING gist (tbl_id WITH &&);"

    violations: core.ViolationMetric = lint_invalid_exclusion_constraint_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_valid_exclusion_constraint_name(
    lint_invalid_exclusion_constraint_name: core.Linter,
) -> None:
    """Test pass valid exclusion constraint name."""
    sql_pass: str = """
    CREATE TABLE tbl (tbl_id bigint,
    CONSTRAINT tbl_tbl_id_exclusion EXCLUDE USING gist (tbl_id WITH &&));
    """

    violations: core.ViolationMetric = lint_invalid_exclusion_constraint_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_invalid_exclusion_constraint_name(
    lint_invalid_exclusion_constraint_name: core.Linter,
) -> None:
    """Test fail invalid exclusion constraint name."""
    sql_fail: str = """
    ALTER TABLE tbl ADD CONSTRAINT tbl_exclusion EXCLUDE USING gist (tbl_id WITH &&);
    """

    violations: core.ViolationMetric = lint_invalid_exclusion_constraint_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_invalid_exclusion_constraint_name_description(
    lint_invalid_exclusion_constraint_name: core.Linter,
    invalid_exclusion_constraint_name: core.BaseChecker,
) -> None:
    """Test invalid exclusion constraint name description."""
    sql_fail: str = """
    CREATE TABLE tbl (tbl_id bigint,
    CONSTRAINT tbl_exclusion EXCLUDE USING gist (tbl_id WITH &&));
    """

    _: core.ViolationMetric = lint_invalid_exclusion_constraint_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(invalid_exclusion_constraint_name.violations),
        ).description
        == f"Exclusion constraint `tbl_exclusion` does not follow naming convention `{invalid_exclusion_constraint_name.config.lint.regex_constraint_exclusion}`"  # noqa: E501
    )


def test_pass_noqa_invalid_exclusion_constraint_name(
    lint_invalid_exclusion_constraint_name: core.Linter,
) -> None:
    """Test pass noqa invalid exclusion constraint name."""
    sql_pass_noqa: str = """
    -- noqa: NM006
    ALTER TABLE tbl ADD CONSTRAINT tbl_exclusion EXCLUDE USING gist (tbl_id WITH &&);
    """

    violations: core.ViolationMetric = lint_invalid_exclusion_constraint_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_invalid_exclusion_constraint_name(
    lint_invalid_exclusion_constraint_name: core.Linter,
) -> None:
    """Test fail noqa invalid exclusion constraint name."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE tbl (tbl_id bigint,
    CONSTRAINT key_tbl EXCLUDE USING gist (tbl_id WITH &&));
    """

    violations: core.ViolationMetric = lint_invalid_exclusion_constraint_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_invalid_exclusion_constraint_name(
    lint_invalid_exclusion_constraint_name: core.Linter,
) -> None:
    """Test pass noqa invalid exclusion constraint name."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (tbl_id bigint,
    CONSTRAINT tbl_exclusion EXCLUDE USING gist (tbl_id WITH &&));
    """

    violations: core.ViolationMetric = lint_invalid_exclusion_constraint_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
