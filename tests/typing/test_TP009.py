"""Test usage of integer."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.typing.TP009 import Integer


@pytest.fixture(scope="module")
def integer() -> core.BaseChecker:
    """Create an instance of integer."""
    core.add_apply_fix_to_rule(Integer)
    core.add_set_locations_to_rule(Integer)
    return Integer()


@pytest.fixture
def lint_integer(
    linter: core.Linter,
    integer: core.BaseChecker,
) -> core.Linter:
    """Lint integer."""
    integer.config.lint.fix = False
    linter.checkers.add(integer)

    return linter


def test_integer_rule_code(
    integer: core.BaseChecker,
) -> None:
    """Test integer rule code."""
    assert integer.code == integer.__module__.split(".")[-1]


def test_integer_auto_fixable(
    integer: core.BaseChecker,
) -> None:
    """Test integer auto fixable."""
    assert integer.is_auto_fixable is True


def test_pass_create_table_bigint(
    lint_integer: core.Linter,
) -> None:
    """Test pass bigint."""
    sql_fail: str = "CREATE TABLE tbl (retry_count bigint);"

    violations: core.ViolationMetric = lint_integer.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_bigint(
    lint_integer: core.Linter,
) -> None:
    """Test pass bigint."""
    sql_fail: str = """
    ALTER TABLE tbl ADD COLUMN retry_count bigint;
    """

    violations: core.ViolationMetric = lint_integer.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_integer(
    lint_integer: core.Linter,
) -> None:
    """Test fail create table integer."""
    sql_fail: str = "CREATE TABLE tbl (retry_count integer);"

    violations: core.ViolationMetric = lint_integer.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_integer(
    lint_integer: core.Linter,
) -> None:
    """Test fail alter table integer."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN retry_count integer;"

    violations: core.ViolationMetric = lint_integer.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_integer_description(
    lint_integer: core.Linter,
    integer: core.BaseChecker,
) -> None:
    """Test integer description."""
    sql_fail: str = "CREATE TABLE tbl (retry_count integer);"

    _: core.ViolationMetric = lint_integer.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(integer.violations),
        ).description
        == "Prefer bigint over integer"
    )


def test_pass_noqa_integer(
    lint_integer: core.Linter,
) -> None:
    """Test pass noqa integer."""
    sql_pass_noqa: str = """
    -- noqa: TP009
    CREATE TABLE tbl (tbl_id int, retry_count integer)
    """

    violations: core.ViolationMetric = lint_integer.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_integer(
    lint_integer: core.Linter,
) -> None:
    """Test fail noqa integer."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN retry_count integer;
    """

    violations: core.ViolationMetric = lint_integer.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_integer(
    lint_integer: core.Linter,
) -> None:
    """Test pass noqa integer."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (tbl_id int, retry_count integer);
    """

    violations: core.ViolationMetric = lint_integer.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_integer(
    lint_integer: core.Linter,
    integer: core.BaseChecker,
) -> None:
    """Test fail fix integer."""
    sql_fail: str = "CREATE TABLE tbl (user_id uuid, retry_count integer);"

    sql_fix: str = "CREATE TABLE tbl (\n    user_id uuid\n  , retry_count bigint\n);"

    integer.config.lint.fix = True

    violations: core.ViolationMetric = lint_integer.run(
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


def test_fail_fix_alter_table_integer(
    lint_integer: core.Linter,
    integer: core.BaseChecker,
) -> None:
    """Test fail fix integer."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN retry_count int;"

    sql_fix: str = "ALTER TABLE tbl\n    ADD COLUMN retry_count bigint;"

    integer.config.lint.fix = True

    violations: core.ViolationMetric = lint_integer.run(
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
