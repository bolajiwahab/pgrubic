"""Test update without where clause."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN022 import UpdateWithoutWhereClause


@pytest.fixture(scope="module")
def update_without_where_clause() -> core.BaseChecker:
    """Create an instance of UpdateWithoutWhereClause."""
    core.add_set_locations_to_rule(UpdateWithoutWhereClause)
    return UpdateWithoutWhereClause()


@pytest.fixture
def lint_update_without_where_clause(
    linter: core.Linter,
    update_without_where_clause: core.BaseChecker,
) -> core.Linter:
    """Lint UpdateWithoutWhereClause."""
    linter.checkers.add(update_without_where_clause)

    return linter


def test_update_without_where_clause_rule_code(
    update_without_where_clause: core.BaseChecker,
) -> None:
    """Test update without where clause rule code."""
    assert (
        update_without_where_clause.code
        == update_without_where_clause.__module__.split(".")[-1]
    )


def test_update_without_where_clause_auto_fixable(
    update_without_where_clause: core.BaseChecker,
) -> None:
    """Test update without where clause auto fixable."""
    assert update_without_where_clause.is_auto_fixable is False


def test_pass_update_with_where_clause(
    lint_update_without_where_clause: core.Linter,
) -> None:
    """Test pass update without where clause."""
    sql_pass: str = "UPDATE measurement SET city_id = 1 WHERE city_id = 10;"

    violations: core.ViolationMetric = lint_update_without_where_clause.run(
        file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_update_without_where_clause(
    lint_update_without_where_clause: core.Linter,
) -> None:
    """Test fail update without where clause."""
    sql_fail: str = "UPDATE measurement SET city_id = 1;"

    violations: core.ViolationMetric = lint_update_without_where_clause.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_update_without_where_clause_description(
    lint_update_without_where_clause: core.Linter,
    update_without_where_clause: core.BaseChecker,
) -> None:
    """Test update without where clause description."""
    sql_fail: str = "UPDATE measurement SET city_id = 1;"

    _: core.ViolationMetric = lint_update_without_where_clause.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(update_without_where_clause.violations),
        ).description
        == "Found UPDATE without a WHERE clause"
    )


def test_pass_noqa_update_without_where_clause(
    lint_update_without_where_clause: core.Linter,
) -> None:
    """Test pass noqa update without where clause."""
    sql_pass_noqa: str = """
    -- noqa: GN022
    UPDATE measurement SET city_id = 1;
    """

    violations: core.ViolationMetric = lint_update_without_where_clause.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_update_without_where_clause(
    lint_update_without_where_clause: core.Linter,
) -> None:
    """Test fail noqa update without where clause."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    UPDATE measurement SET city_id = 1;
    """

    violations: core.ViolationMetric = lint_update_without_where_clause.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_update_without_where_clause(
    lint_update_without_where_clause: core.Linter,
) -> None:
    """Test fail noqa update without where clause."""
    sql_pass_noqa: str = """
    -- noqa
    UPDATE measurement SET city_id = 1;
    """

    violations: core.ViolationMetric = lint_update_without_where_clause.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
