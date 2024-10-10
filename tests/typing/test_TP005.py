"""Test usage of varchar."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.typing.TP005 import Varchar


@pytest.fixture(scope="module")
def varchar() -> core.BaseChecker:
    """Create an instance of varchar."""
    core.add_apply_fix_to_rule(Varchar)
    core.add_set_locations_to_rule(Varchar)
    return Varchar()


@pytest.fixture
def lint_varchar(
    linter: core.Linter,
    varchar: core.BaseChecker,
) -> core.Linter:
    """Lint varchar."""
    varchar.config.lint.fix = False
    linter.checkers.add(varchar)

    return linter


def test_varchar_rule_code(
    varchar: core.BaseChecker,
) -> None:
    """Test varchar rule code."""
    assert varchar.code == varchar.__module__.split(".")[-1]


def test_varchar_auto_fixable(
    varchar: core.BaseChecker,
) -> None:
    """Test varchar auto fixable."""
    assert varchar.is_auto_fixable is True


def test_pass_create_table_text(
    lint_varchar: core.Linter,
) -> None:
    """Test pass text."""
    sql_fail: str = "CREATE TABLE music (first_name text);"

    violations: core.ViolationMetric = lint_varchar.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_text(
    lint_varchar: core.Linter,
) -> None:
    """Test pass varchar."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN last_name text;"

    violations: core.ViolationMetric = lint_varchar.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_varchar(
    lint_varchar: core.Linter,
) -> None:
    """Test fail create table varchar."""
    sql_fail: str = "CREATE TABLE music (first_name varchar(20));"

    violations: core.ViolationMetric = lint_varchar.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_varchar(
    lint_varchar: core.Linter,
) -> None:
    """Test fail alter table varchar."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN last_name varchar;"

    violations: core.ViolationMetric = lint_varchar.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_varchar_description(
    lint_varchar: core.Linter,
    varchar: core.BaseChecker,
) -> None:
    """Test varchar description."""
    sql_fail: str = "CREATE TABLE music (middle_name varchar(0));"

    _: core.ViolationMetric = lint_varchar.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(varchar.violations),
        ).description
        == "Prefer text to varchar"
    )


def test_pass_noqa_varchar(
    lint_varchar: core.Linter,
) -> None:
    """Test pass noqa varchar."""
    sql_pass_noqa: str = """
    -- noqa: TP005
    CREATE TABLE music (age int, birth_place varchar)
    """

    violations: core.ViolationMetric = lint_varchar.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_varchar(
    lint_varchar: core.Linter,
) -> None:
    """Test fail noqa varchar."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE music ADD COLUMN birth_place varchar(10);
    """

    violations: core.ViolationMetric = lint_varchar.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_varchar(
    lint_varchar: core.Linter,
) -> None:
    """Test pass noqa varchar."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE music (age int, first_name varchar);
    """

    violations: core.ViolationMetric = lint_varchar.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_varchar(
    lint_varchar: core.Linter,
    varchar: core.BaseChecker,
) -> None:
    """Test fail fix varchar."""
    sql_fail: str = "CREATE TABLE music (age int, first_name varchar(255));"

    sql_fix: str = "CREATE TABLE music (\n    age integer\n  , first_name text\n);"

    varchar.config.lint.fix = True

    violations: core.ViolationMetric = lint_varchar.run(
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


def test_fail_fix_alter_table_varchar(
    lint_varchar: core.Linter,
    varchar: core.BaseChecker,
) -> None:
    """Test fail fix varchar."""
    sql_fail: str = "ALTER TABLE music ADD COLUMN last_name varchar;"

    sql_fix: str = "ALTER TABLE music\n    ADD COLUMN last_name text;"

    varchar.config.lint.fix = True

    violations: core.ViolationMetric = lint_varchar.run(
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
