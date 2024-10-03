"""Test usage of char."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.typing.TP004 import Char


@pytest.fixture(scope="module")
def char() -> core.BaseChecker:
    """Create an instance of Char."""
    core.add_apply_fix_to_rule(Char)
    core.add_set_locations_to_rule(Char)
    return Char()


@pytest.fixture
def lint_char(
    linter: core.Linter,
    char: core.BaseChecker,
) -> core.Linter:
    """Lint Char."""
    char.config.lint.fix = False
    linter.checkers.add(char)

    return linter


def test_char_rule_code(
    char: core.BaseChecker,
) -> None:
    """Test char rule code."""
    assert char.code == char.__module__.split(".")[-1]


def test_char_auto_fixable(
    char: core.BaseChecker,
) -> None:
    """Test char auto fixable."""
    assert char.is_auto_fixable is True


def test_pass_create_table_timestamp_with_timezone(
    lint_char: core.Linter,
) -> None:
    """Test pass char."""
    sql_fail: str = "CREATE TABLE music (first_name text);"

    violations: core.ViolationMetric = lint_char.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_timestamp_with_timezone(
    lint_char: core.Linter,
) -> None:
    """Test pass char."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN last_name text;"

    violations: core.ViolationMetric = lint_char.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_char(
    lint_char: core.Linter,
) -> None:
    """Test fail create table char."""
    sql_fail: str = "CREATE TABLE music (first_name char(0));"

    violations: core.ViolationMetric = lint_char.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_char(
    lint_char: core.Linter,
) -> None:
    """Test fail alter table char."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN last_name char;"

    violations: core.ViolationMetric = lint_char.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_char_description(
    lint_char: core.Linter,
    char: core.BaseChecker,
) -> None:
    """Test char description."""
    sql_fail: str = "CREATE TABLE music (middle_name char(0));"

    _: core.ViolationMetric = lint_char.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(char.violations),
        ).description
        == "Prefer text to char"
    )


def test_pass_noqa_char(
    lint_char: core.Linter,
) -> None:
    """Test pass noqa char."""
    sql_pass_noqa: str = """
    -- noqa: TP004
    CREATE TABLE music (age int, birth_place char)
    """

    violations: core.ViolationMetric = lint_char.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_char(
    lint_char: core.Linter,
) -> None:
    """Test fail noqa char."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE music ADD COLUMN birth_place char(0);
    """

    violations: core.ViolationMetric = lint_char.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_char(
    lint_char: core.Linter,
) -> None:
    """Test pass noqa char."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE music (age int, first_name char);
    """

    violations: core.ViolationMetric = lint_char.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_char(
    lint_char: core.Linter,
    char: core.BaseChecker,
) -> None:
    """Test fail fix char."""
    sql_fail: str = "CREATE TABLE music (age int, first_name char(0));"

    sql_fix: str = "CREATE TABLE music (\n    age integer\n  , first_name text\n);"

    char.config.lint.fix = True

    violations: core.ViolationMetric = lint_char.run(
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


def test_fail_fix_alter_table_char(
    lint_char: core.Linter,
    char: core.BaseChecker,
) -> None:
    """Test fail fix char."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN last_name char;"

    sql_fix: str = "ALTER TABLE music\n    ADD COLUMN last_name text;"

    char.config.lint.fix = True

    violations: core.ViolationMetric = lint_char.run(
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
