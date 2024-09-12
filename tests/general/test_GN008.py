"""Test for missing replace in procedure."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.general.GN008 import MissingReplaceInProcedure


@pytest.fixture(scope="module")
def missing_replace_in_procedure() -> core.BaseChecker:
    """Create an instance of MissingReplaceInProcedure."""
    core.add_apply_fix_to_rule(MissingReplaceInProcedure)
    core.add_set_locations_to_rule(MissingReplaceInProcedure)
    return MissingReplaceInProcedure()


@pytest.fixture
def lint_missing_replace_in_procedure(
    linter: core.Linter,
    missing_replace_in_procedure: core.BaseChecker,
) -> core.Linter:
    """Lint MissingReplaceInProcedure."""
    missing_replace_in_procedure.config.lint.fix = False
    linter.checkers.add(missing_replace_in_procedure)

    return linter


def test_missing_replace_in_procedure_rule_code(
    missing_replace_in_procedure: core.BaseChecker,
) -> None:
    """Test missing replace in procedure rule code."""
    assert (
        missing_replace_in_procedure.code
        == missing_replace_in_procedure.__module__.split(".")[-1]
    )


def test_missing_replace_in_procedure_auto_fixable(
    missing_replace_in_procedure: core.BaseChecker,
) -> None:
    """Test missing replace in procedure auto fixable."""
    assert missing_replace_in_procedure.is_auto_fixable is True


def test_pass_create_or_replace_in_function(
    lint_missing_replace_in_procedure: core.Linter,
) -> None:
    """Test fail missing replace in procedure."""
    sql_fail: str = """
    CREATE OR REPLACE PROCEDURE dup(int) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_procedure.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_missing_replace_in_procedure(
    lint_missing_replace_in_procedure: core.Linter,
) -> None:
    """Test fail missing replace in procedure."""
    sql_fail: str = """
    CREATE PROCEDURE dup(int) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_procedure.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_missing_replace_in_procedure_description(
    lint_missing_replace_in_procedure: core.Linter,
    missing_replace_in_procedure: core.BaseChecker,
) -> None:
    """Test missing replace in procedure description."""
    sql_fail: str = """
    CREATE PROCEDURE dup(int) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    _: core.ViolationMetric = lint_missing_replace_in_procedure.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(missing_replace_in_procedure.violations),
        ).description
        == "Prefer create or replace for procedure"
    )


def test_pass_noqa_missing_replace_in_procedure(
    lint_missing_replace_in_procedure: core.Linter,
) -> None:
    """Test pass noqa missing replace in procedure."""
    sql_pass_noqa: str = """
    -- noqa: GN008
    CREATE PROCEDURE dup(int) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_procedure.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_missing_replace_in_procedure(
    lint_missing_replace_in_procedure: core.Linter,
) -> None:
    """Test fail noqa missing replace in procedure."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE PROCEDURE dup(int) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_procedure.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_missing_replace_in_procedure(
    lint_missing_replace_in_procedure: core.Linter,
) -> None:
    """Test fail noqa missing replace in procedure."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE PROCEDURE dup(int) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    violations: core.ViolationMetric = lint_missing_replace_in_procedure.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_missing_replace_in_procedure(
    lint_missing_replace_in_procedure: core.Linter,
    missing_replace_in_procedure: core.BaseChecker,
) -> None:
    """Test fail fix missing replace in procedure."""
    sql_fail: str = """
    CREATE PROCEDURE dup(int) LANGUAGE SQL
    AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$
    ;
    """

    sql_fix: str = (
        "CREATE OR REPLACE PROCEDURE dup(integer)\nLANGUAGE sql\nAS $$ SELECT $1, CAST($1 AS text) || ' is text' $$;"  # noqa: E501
    )

    missing_replace_in_procedure.config.lint.fix = True

    violations: core.ViolationMetric = lint_missing_replace_in_procedure.run(
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
