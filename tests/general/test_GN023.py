"""Test for delete without where clause."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.general.GN023 import DeleteWithoutWhereClause


@pytest.fixture(scope="module")
def delete_without_where_clause() -> core.BaseChecker:
    """Create an instance of DeleteWithoutWhereClause."""
    core.add_set_locations_to_rule(DeleteWithoutWhereClause)
    return DeleteWithoutWhereClause()


@pytest.fixture
def lint_delete_without_where_clause(
    linter: core.Linter,
    delete_without_where_clause: core.BaseChecker,
) -> core.Linter:
    """Lint DeleteWithoutWhereClause."""
    linter.checkers.add(delete_without_where_clause)

    return linter


def test_delete_without_where_clause_rule_code(
    delete_without_where_clause: core.BaseChecker,
) -> None:
    """Test delete without where clause rule code."""
    assert (
        delete_without_where_clause.code
        == delete_without_where_clause.__module__.split(".")[-1]
    )


def test_delete_without_where_clause_auto_fixable(
    delete_without_where_clause: core.BaseChecker,
) -> None:
    """Test delete without where clause auto fixable."""
    assert delete_without_where_clause.is_auto_fixable is False


def test_pass_update_with_where_clause(
    lint_delete_without_where_clause: core.Linter,
) -> None:
    """Test pass delete without where clause."""
    sql_pass: str = "DELETE FROM measurement WHERE city_id = 10;"

    violations: core.ViolationMetric = lint_delete_without_where_clause.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_delete_without_where_clause(
    lint_delete_without_where_clause: core.Linter,
) -> None:
    """Test fail delete without where clause."""
    sql_fail: str = "DELETE FROM measurement;"

    violations: core.ViolationMetric = lint_delete_without_where_clause.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_delete_without_where_clause_description(
    lint_delete_without_where_clause: core.Linter,
    delete_without_where_clause: core.BaseChecker,
) -> None:
    """Test delete without where clause description."""
    sql_fail: str = "DELETE FROM measurement;"

    _: core.ViolationMetric = lint_delete_without_where_clause.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(delete_without_where_clause.violations),
        ).description
        == "Found DELETE without a WHERE clause"
    )


def test_pass_noqa_delete_without_where_clause(
    lint_delete_without_where_clause: core.Linter,
) -> None:
    """Test pass noqa delete without where clause."""
    sql_pass_noqa: str = """
    -- noqa: GN023
    DELETE FROM measurement;
    """

    violations: core.ViolationMetric = lint_delete_without_where_clause.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_delete_without_where_clause(
    lint_delete_without_where_clause: core.Linter,
) -> None:
    """Test fail noqa delete without where clause."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    DELETE FROM measurement;
    """

    violations: core.ViolationMetric = lint_delete_without_where_clause.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_delete_without_where_clause(
    lint_delete_without_where_clause: core.Linter,
) -> None:
    """Test fail noqa delete without where clause."""
    sql_pass_noqa: str = """
    -- noqa:
    DELETE FROM measurement;
    """

    violations: core.ViolationMetric = lint_delete_without_where_clause.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
