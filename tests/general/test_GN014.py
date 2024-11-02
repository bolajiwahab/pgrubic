"""Test select into."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN014 import SelectInto


@pytest.fixture(scope="module")
def select_into() -> core.BaseChecker:
    """Create an instance of SelectInto."""
    core.add_apply_fix_to_rule(SelectInto)
    core.add_set_locations_to_rule(SelectInto)
    return SelectInto()


@pytest.fixture
def lint_select_into(
    linter: core.Linter,
    select_into: core.BaseChecker,
) -> core.Linter:
    """Lint SelectInto."""
    select_into.config.lint.fix = False
    linter.checkers.add(select_into)

    return linter


def test_select_into_rule_code(
    select_into: core.BaseChecker,
) -> None:
    """Test select into rule code."""
    assert select_into.code == select_into.__module__.split(".")[-1]


def test_select_into_auto_fixable(
    select_into: core.BaseChecker,
) -> None:
    """Test select into auto fixable."""
    assert select_into.is_auto_fixable is True


def test_pass_create_table_as(
    lint_select_into: core.Linter,
) -> None:
    """Test fail select into."""
    sql_fail: str = (
        "CREATE TABLE tbl AS SELECT * FROM films WHERE created_at >= '2002-01-01';"
    )

    violations: core.ViolationMetric = lint_select_into.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_select_into(
    lint_select_into: core.Linter,
) -> None:
    """Test fail select into."""
    sql_fail: str = (
        "SELECT * INTO films_recent FROM films WHERE created_at >= '2002-01-01';"
    )

    violations: core.ViolationMetric = lint_select_into.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_select_into_description(
    lint_select_into: core.Linter,
    select_into: core.BaseChecker,
) -> None:
    """Test select into description."""
    sql_fail: str = (
        "SELECT * INTO films_recent FROM films WHERE created_at >= '2002-01-01';"
    )

    _: core.ViolationMetric = lint_select_into.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(select_into.violations),
        ).description
        == "Use CREATE TABLE AS instead of SELECT INTO"
    )


def test_pass_noqa_select_into(
    lint_select_into: core.Linter,
) -> None:
    """Test pass noqa select into."""
    sql_pass_noqa: str = """
    -- noqa: GN014
    SELECT * INTO films_recent FROM films WHERE created_at >= '2002-01-01';
    """

    violations: core.ViolationMetric = lint_select_into.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_select_into(
    lint_select_into: core.Linter,
) -> None:
    """Test fail noqa select into."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    SELECT * INTO films_recent FROM films WHERE created_at >= '2002-01-01';
    """

    violations: core.ViolationMetric = lint_select_into.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_select_into(
    lint_select_into: core.Linter,
) -> None:
    """Test fail noqa select into."""
    sql_pass_noqa: str = """
    -- noqa
    SELECT * INTO films_recent FROM films WHERE created_at >= '2002-01-01';
    """

    violations: core.ViolationMetric = lint_select_into.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_select_into(
    lint_select_into: core.Linter,
    select_into: core.BaseChecker,
) -> None:
    """Test fail fix select into."""
    sql_fail: str = (
        "SELECT * INTO films_recent FROM films WHERE created_at >= '2002-01-01';"
    )

    sql_fix: str = "CREATE TABLE films_recent AS\nSELECT *\n  FROM films\n WHERE created_at >= '2002-01-01';\n"  # noqa: E501

    select_into.config.lint.fix = True

    violations: core.ViolationMetric = lint_select_into.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
