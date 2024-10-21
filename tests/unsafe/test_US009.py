"""Test drop schema."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US009 import DropSchema


@pytest.fixture(scope="module")
def drop_schema() -> core.BaseChecker:
    """Create an instance of DropSchema."""
    core.add_set_locations_to_rule(DropSchema)
    return DropSchema()


@pytest.fixture
def lint_drop_schema(
    linter: core.Linter,
    drop_schema: core.BaseChecker,
) -> core.Linter:
    """Lint DropSchema."""
    linter.checkers.add(drop_schema)

    return linter


def test_drop_schema_rule_code(drop_schema: core.BaseChecker) -> None:
    """Test drop schema rule code."""
    assert drop_schema.code == drop_schema.__module__.split(".")[-1]


def test_drop_schema_auto_fixable(drop_schema: core.BaseChecker) -> None:
    """Test drop schema auto fixable."""
    assert drop_schema.is_auto_fixable is False


def test_fail_drop_schema(lint_drop_schema: core.Linter) -> None:
    """Test fail drop schema."""
    sql_fail: str = """
    DROP schema test
    ;
    """

    violations: core.ViolationMetric = lint_drop_schema.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_drop_schema_description(
    lint_drop_schema: core.Linter,
    drop_schema: core.BaseChecker,
) -> None:
    """Test fail drop schema description."""
    sql_fail: str = """
    DROP schema test
    ;
    """

    _: core.ViolationMetric = lint_drop_schema.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert next(iter(drop_schema.violations)).description == "Drop schema detected"


def test_pass_noqa_drop_schema(lint_drop_schema: core.Linter) -> None:
    """Test pass noqa schema."""
    sql_pass_noqa: str = """
    DROP schema test -- noqa: US009
    ;
    """

    violations: core.ViolationMetric = lint_drop_schema.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_drop_schema(lint_drop_schema: core.Linter) -> None:
    """Test fail noqa drop schema."""
    sql_noqa: str = """
    DROP schema test -- noqa: US002
    ;
    """

    violations: core.ViolationMetric = lint_drop_schema.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_drop_schema(
    lint_drop_schema: core.Linter,
) -> None:
    """Test fail noqa drop schema."""
    sql_noqa: str = """
    DROP schema test -- noqa
    ;
    """

    violations: core.ViolationMetric = lint_drop_schema.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
