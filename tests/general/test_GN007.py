"""Test for missing replace in function."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.general.GN007 import MissingReplaceInFunction


@pytest.fixture(scope="module")
def missing_replace_in_function() -> core.BaseChecker:
    """Create an instance of MissingReplaceInFunction."""
    core.add_apply_fix_to_rule(MissingReplaceInFunction)
    return MissingReplaceInFunction()


@pytest.fixture
def lint_missing_replace_in_function(
    linter: core.Linter,
    missing_replace_in_function: core.BaseChecker,
) -> core.Linter:
    """Lint MissingReplaceInFunction."""
    missing_replace_in_function.config.lint.fix = False
    linter.checkers.add(missing_replace_in_function)

    return linter


def test_missing_replace_in_function_rule_code(
    missing_replace_in_function: core.BaseChecker,
) -> None:
    """Test missing replace in function rule code."""
    assert (
        missing_replace_in_function.code
        == missing_replace_in_function.__module__.split(".")[-1]
    )


def test_missing_replace_in_function_auto_fixable(
    missing_replace_in_function: core.BaseChecker,
) -> None:
    """Test missing replace in function auto fixable."""
    assert missing_replace_in_function.is_auto_fixable is True


def test_pass_create_or_replace_in_function(
    lint_missing_replace_in_function: core.Linter,
) -> None:
    """Test fail missing replace in function."""
    sql_fail: str = """
    CREATE OR REPLACE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_function.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_missing_replace_in_function(
    lint_missing_replace_in_function: core.Linter,
) -> None:
    """Test fail missing replace in function."""
    sql_fail: str = """
    CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_function.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_missing_replace_in_function_description(
    lint_missing_replace_in_function: core.Linter,
    missing_replace_in_function: core.BaseChecker,
) -> None:
    """Test missing replace in function description."""
    sql_fail: str = """
    CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    _: core.ViolationMetric = lint_missing_replace_in_function.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(missing_replace_in_function.violations),
        ).description
        == "Prefer create or replace for function"
    )


def test_pass_noqa_missing_replace_in_function(
    lint_missing_replace_in_function: core.Linter,
) -> None:
    """Test pass noqa missing replace in function."""
    sql_pass_noqa: str = """
    -- noqa: GN007
    CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_function.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_missing_replace_in_function(
    lint_missing_replace_in_function: core.Linter,
) -> None:
    """Test fail noqa missing replace in function."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_function.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_missing_replace_in_function(
    lint_missing_replace_in_function: core.Linter,
) -> None:
    """Test fail noqa missing replace in function."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_function.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_missing_replace_in_function(
    lint_missing_replace_in_function: core.Linter,
    missing_replace_in_function: core.BaseChecker,
) -> None:
    """Test fail fix missing replace in function."""
    sql_fail: str = """
    CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    sql_fix: str = (
        "CREATE OR REPLACE FUNCTION dup(integer)\nRETURNS TABLE (f1 integer, f2 text)\nLANGUAGE sql\nAS $$ SELECT $1, CAST($1 AS text) || ' is text' $$;"  # noqa: E501
    )

    missing_replace_in_function.config.lint.fix = True

    violations: core.ViolationMetric = lint_missing_replace_in_function.run(
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
