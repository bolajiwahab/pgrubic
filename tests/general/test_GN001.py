"""Test table inheritance."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN001 import TableInheritance


@pytest.fixture(scope="module")
def table_inheritance() -> core.BaseChecker:
    """Create an instance of TableInheritance."""
    core.add_set_locations_to_rule(TableInheritance)
    return TableInheritance()


@pytest.fixture
def lint_table_inheritance(
    linter: core.Linter,
    table_inheritance: core.BaseChecker,
) -> core.Linter:
    """Lint TableInheritance."""
    linter.checkers.add(table_inheritance)

    return linter


def test_table_inheritance_rule_code(
    table_inheritance: core.BaseChecker,
) -> None:
    """Test table inheritance rule code."""
    assert table_inheritance.code == table_inheritance.__module__.split(".")[-1]


def test_table_inheritance_auto_fixable(
    table_inheritance: core.BaseChecker,
) -> None:
    """Test table inheritance auto fixable."""
    assert table_inheritance.is_auto_fixable is False


def test_fail_table_inheritance(
    lint_table_inheritance: core.Linter,
) -> None:
    """Test fail table inheritance."""
    sql_fail: str = "CREATE TABLE measurement_y2006m02 () INHERITS (measurement);"

    violations: core.ViolationMetric = lint_table_inheritance.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_table_inheritance_description(
    lint_table_inheritance: core.Linter,
    table_inheritance: core.BaseChecker,
) -> None:
    """Test table inheritance description."""
    sql_fail: str = "CREATE TABLE measurement_y2006m02 () INHERITS (measurement);"

    _: core.ViolationMetric = lint_table_inheritance.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(table_inheritance.violations),
        ).description
        == "Table inheritance detected"
    )


def test_pass_noqa_table_inheritance(
    lint_table_inheritance: core.Linter,
) -> None:
    """Test pass noqa table inheritance."""
    sql_pass_noqa: str = """
    -- noqa: GN001
    CREATE TABLE measurement_y2006m02 () INHERITS (measurement);
    """

    violations: core.ViolationMetric = lint_table_inheritance.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_table_inheritance(
    lint_table_inheritance: core.Linter,
) -> None:
    """Test fail noqa table inheritance."""
    sql_fail_noqa: str = """
    -- noqa: GN002
    CREATE TABLE measurement_y2006m02 () INHERITS (measurement);
    """

    violations: core.ViolationMetric = lint_table_inheritance.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_table_inheritance(
    lint_table_inheritance: core.Linter,
) -> None:
    """Test fail noqa table inheritance."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE measurement_y2006m02 () INHERITS (measurement);
    """

    violations: core.ViolationMetric = lint_table_inheritance.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
