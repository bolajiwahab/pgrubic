"""Test for sql_ascii encoding."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.general.GN003 import SqlAsciiEncoding


@pytest.fixture(scope="module")
def sql_ascii_encoding() -> core.BaseChecker:
    """Create an instance of SqlAsciiEncoding."""
    core.add_apply_fix_to_rule(SqlAsciiEncoding)
    core.add_set_locations_to_rule(SqlAsciiEncoding)
    return SqlAsciiEncoding()


@pytest.fixture
def lint_sql_ascii_encoding(
    linter: core.Linter,
    sql_ascii_encoding: core.BaseChecker,
) -> core.Linter:
    """Lint SqlAsciiEncoding."""
    sql_ascii_encoding.config.lint.fix = False
    linter.checkers.add(sql_ascii_encoding)

    return linter


def test_sql_ascii_encoding_rule_code(
    sql_ascii_encoding: core.BaseChecker,
) -> None:
    """Test sql_ascii encoding rule code."""
    assert sql_ascii_encoding.code == sql_ascii_encoding.__module__.split(".")[-1]


def test_sql_ascii_encoding_auto_fixable(
    sql_ascii_encoding: core.BaseChecker,
) -> None:
    """Test sql_ascii encoding auto fixable."""
    assert sql_ascii_encoding.is_auto_fixable is True


def test_pass_encoding(
    lint_sql_ascii_encoding: core.Linter,
) -> None:
    """Test fail sql_ascii encoding."""
    sql_fail: str = "CREATE DATABASE music ENCODING UTF8 TEMPLATE template0;"

    violations: core.ViolationMetric = lint_sql_ascii_encoding.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_sql_ascii_encoding(
    lint_sql_ascii_encoding: core.Linter,
) -> None:
    """Test fail sql_ascii encoding."""
    sql_fail: str = "CREATE DATABASE music ENCODING SQL_ASCII TEMPLATE template0;"

    violations: core.ViolationMetric = lint_sql_ascii_encoding.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_sql_ascii_encoding_description(
    lint_sql_ascii_encoding: core.Linter,
    sql_ascii_encoding: core.BaseChecker,
) -> None:
    """Test sql_ascii encoding description."""
    sql_fail: str = "CREATE DATABASE music ENCODING SQL_ASCII TEMPLATE template0;"

    _: core.ViolationMetric = lint_sql_ascii_encoding.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(sql_ascii_encoding.violations),
        ).description
        == "SQL_ASCII encoding detected"
    )


def test_pass_noqa_sql_ascii_encoding(
    lint_sql_ascii_encoding: core.Linter,
) -> None:
    """Test pass noqa sql_ascii encoding."""
    sql_pass_noqa: str = """
    -- noqa: GN003
    CREATE DATABASE music ENCODING SQL_ASCII TEMPLATE template0;
    """

    violations: core.ViolationMetric = lint_sql_ascii_encoding.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_sql_ascii_encoding(
    lint_sql_ascii_encoding: core.Linter,
) -> None:
    """Test fail noqa sql_ascii encoding."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE DATABASE music ENCODING SQL_ASCII TEMPLATE template0;
    """

    violations: core.ViolationMetric = lint_sql_ascii_encoding.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_sql_ascii_encoding(
    lint_sql_ascii_encoding: core.Linter,
) -> None:
    """Test fail noqa sql_ascii encoding."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE DATABASE music ENCODING SQL_ASCII TEMPLATE template0;
    """

    violations: core.ViolationMetric = lint_sql_ascii_encoding.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_sql_ascii_encoding(
    lint_sql_ascii_encoding: core.Linter,
    sql_ascii_encoding: core.BaseChecker,
) -> None:
    """Test fail fix sql_ascii encoding."""
    sql_fail: str = "CREATE DATABASE music ENCODING SQL_ASCII TEMPLATE template0"

    sql_fix: str = (
        "CREATE DATABASE music\n  WITH encoding = 'utf8'\n       template = 'template0';"
    )

    sql_ascii_encoding.config.lint.fix = True

    violations: core.ViolationMetric = lint_sql_ascii_encoding.run(
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
