"""Test drop database."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.US008 import DropDatabase


@pytest.fixture(scope="module")
def drop_database() -> core.BaseChecker:
    """Create an instance of DropDatabase."""
    core.add_set_locations_to_rule(DropDatabase)
    return DropDatabase()


@pytest.fixture
def lint_drop_database(
    linter: core.Linter,
    drop_database: core.BaseChecker,
) -> core.Linter:
    """Lint DropDatabase."""
    linter.checkers.add(drop_database)

    return linter


def test_drop_database_rule_code(drop_database: core.BaseChecker) -> None:
    """Test drop database rule code."""
    assert drop_database.code == drop_database.__module__.split(".")[-1]


def test_drop_database_auto_fixable(drop_database: core.BaseChecker) -> None:
    """Test drop database auto fixable."""
    assert drop_database.is_auto_fixable is False


def test_fail_drop_database(lint_drop_database: core.Linter) -> None:
    """Test fail drop database."""
    sql_fail: str = """
    DROP database test
    ;
    """

    violations: core.ViolationMetric = lint_drop_database.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_drop_database_description(
    lint_drop_database: core.Linter,
    drop_database: core.BaseChecker,
) -> None:
    """Test fail drop database description."""
    sql_fail: str = """
    DROP database test
    ;
    """

    _: core.ViolationMetric = lint_drop_database.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert next(iter(drop_database.violations)).description == "Drop database detected"


def test_pass_noqa_drop_database(lint_drop_database: core.Linter) -> None:
    """Test pass noqa database column."""
    sql_pass_noqa: str = """
    DROP database test -- noqa: US008
    ;
    """

    violations: core.ViolationMetric = lint_drop_database.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_drop_database(lint_drop_database: core.Linter) -> None:
    """Test fail noqa drop database."""
    sql_noqa: str = """
    DROP database test -- noqa: US002
    ;
    """

    violations: core.ViolationMetric = lint_drop_database.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_drop_database(
    lint_drop_database: core.Linter,
) -> None:
    """Test fail noqa drop database."""
    sql_noqa: str = """
    DROP database test -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_drop_database.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
