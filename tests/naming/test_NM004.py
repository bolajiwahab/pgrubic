"""Test for invalid foreign key name."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.naming.NM004 import InvalidForeignKeyName


@pytest.fixture(scope="module")
def invalid_foreign_key_name() -> core.BaseChecker:
    """Create an instance of invalid foreign key name."""
    core.add_set_locations_to_rule(InvalidForeignKeyName)
    return InvalidForeignKeyName()


@pytest.fixture
def lint_invalid_foreign_key_name(
    linter: core.Linter,
    invalid_foreign_key_name: core.BaseChecker,
) -> core.Linter:
    """Lint invalid foreign key name."""
    invalid_foreign_key_name.config.lint.regex_index = (
        "[a-zA-Z0-9]+_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_fkey$"
    )

    linter.checkers.add(invalid_foreign_key_name)

    return linter


def test_invalid_foreign_key_name_rule_code(
    invalid_foreign_key_name: core.BaseChecker,
) -> None:
    """Test invalid foreign key name rule code."""
    assert (
        invalid_foreign_key_name.code
        == invalid_foreign_key_name.__module__.split(".")[-1]
    )


def test_invalid_foreign_key_name_auto_fixable(
    invalid_foreign_key_name: core.BaseChecker,
) -> None:
    """Test invalid foreign key name auto fixable."""
    assert invalid_foreign_key_name.is_auto_fixable is False


def test_pass_implicit_foreign_key_name_create_table(
    lint_invalid_foreign_key_name: core.Linter,
) -> None:
    """Test pass implicit foreign key name."""
    sql_fail: str = (
        "CREATE TABLE author (author_id bigint REFERENCES bookstore(author));"
    )

    violations: core.ViolationMetric = lint_invalid_foreign_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_implicit_foreign_key_name_alter_table(
    lint_invalid_foreign_key_name: core.Linter,
) -> None:
    """Test pass implicit foreign key name."""
    sql_fail: str = """
    ALTER TABLE author ADD FOREIGN KEY (author_id) REFERENCES bookstore(author);
    """

    violations: core.ViolationMetric = lint_invalid_foreign_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_valid_foreign_key_name(
    lint_invalid_foreign_key_name: core.Linter,
) -> None:
    """Test pass valid foreign key name."""
    sql_pass: str = """
    CREATE TABLE author (author_id bigint, CONSTRAINT author_author_id_fkey
    FOREIGN KEY (tbl_id) REFERENCES bookstore (author));
    """

    violations: core.ViolationMetric = lint_invalid_foreign_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_invalid_foreign_key_name(
    lint_invalid_foreign_key_name: core.Linter,
) -> None:
    """Test fail invalid foreign key name."""
    sql_fail: str = """
    ALTER TABLE author ADD CONSTRAINT author_key FOREIGN KEY (author_id)
    REFERENCES bookstore (author);
    """

    violations: core.ViolationMetric = lint_invalid_foreign_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_invalid_foreign_key_name_description(
    lint_invalid_foreign_key_name: core.Linter,
    invalid_foreign_key_name: core.BaseChecker,
) -> None:
    """Test invalid foreign key name description."""
    sql_fail: str = """
    CREATE TABLE author (author_id bigint, CONSTRAINT author_fkey FOREIGN KEY (author_id)
    REFERENCES bookstore (author));
    """

    _: core.ViolationMetric = lint_invalid_foreign_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(invalid_foreign_key_name.violations),
        ).description
        == f"Foreign key constraint `author_fkey` does not follow naming convention `{invalid_foreign_key_name.config.lint.regex_constraint_foreign_key}`"  # noqa: E501
    )


def test_pass_noqa_invalid_foreign_key_name(
    lint_invalid_foreign_key_name: core.Linter,
) -> None:
    """Test pass noqa invalid foreign key name."""
    sql_pass_noqa: str = """
    -- noqa: NM004
    ALTER TABLE author ADD CONSTRAINT tbl_key FOREIGN KEY (author_id)
    REFERENCES bookstore (author);
    """

    violations: core.ViolationMetric = lint_invalid_foreign_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_invalid_foreign_key_name(
    lint_invalid_foreign_key_name: core.Linter,
) -> None:
    """Test fail noqa invalid foreign key name."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE author (author_id bigint, CONSTRAINT fkey_author FOREIGN KEY (tbl_id)
    REFERENCES bookstore (author));
    """

    violations: core.ViolationMetric = lint_invalid_foreign_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_invalid_foreign_key_name(
    lint_invalid_foreign_key_name: core.Linter,
) -> None:
    """Test pass noqa invalid foreign key name."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE author (author_id bigint, CONSTRAINT author_fkey FOREIGN KEY (tbl_id)
    REFERENCES bookstore (author));
    """

    violations: core.ViolationMetric = lint_invalid_foreign_key_name.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
