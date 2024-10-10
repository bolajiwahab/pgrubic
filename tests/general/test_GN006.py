"""Test create enum."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.general.GN006 import CreateEnum


@pytest.fixture(scope="module")
def create_enum() -> core.BaseChecker:
    """Create an instance of CreateEnum."""
    core.add_set_locations_to_rule(CreateEnum)
    return CreateEnum()


@pytest.fixture
def lint_create_enum(
    linter: core.Linter,
    create_enum: core.BaseChecker,
) -> core.Linter:
    """Lint CreateEnum."""
    linter.checkers.add(create_enum)

    return linter


def test_create_enum_rule_code(
    create_enum: core.BaseChecker,
) -> None:
    """Test create enum rule code."""
    assert create_enum.code == create_enum.__module__.split(".")[-1]


def test_create_enum_auto_fixable(
    create_enum: core.BaseChecker,
) -> None:
    """Test create enum auto fixable."""
    assert create_enum.is_auto_fixable is False


def test_fail_create_enum(
    lint_create_enum: core.Linter,
) -> None:
    """Test fail create enum."""
    sql_fail: str = "CREATE TYPE mood AS ENUM ('sad', 'ok');"

    violations: core.ViolationMetric = lint_create_enum.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_create_enum_description(
    lint_create_enum: core.Linter,
    create_enum: core.BaseChecker,
) -> None:
    """Test create enum description."""
    sql_fail: str = "CREATE TYPE mood AS ENUM ('sad', 'ok');"

    _: core.ViolationMetric = lint_create_enum.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(create_enum.violations),
        ).description
        == "Prefer mapping table to enum"
    )


def test_pass_noqa_create_enum(
    lint_create_enum: core.Linter,
) -> None:
    """Test pass noqa create enum."""
    sql_pass_noqa: str = """
    -- noqa: GN006
    CREATE TYPE mood AS ENUM ('sad', 'ok');
    """

    violations: core.ViolationMetric = lint_create_enum.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_create_enum(
    lint_create_enum: core.Linter,
) -> None:
    """Test fail noqa create enum."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TYPE mood AS ENUM ('sad', 'ok');
    """

    violations: core.ViolationMetric = lint_create_enum.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_create_enum(
    lint_create_enum: core.Linter,
) -> None:
    """Test fail noqa create enum."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TYPE mood AS ENUM ('sad', 'ok');
    """

    violations: core.ViolationMetric = lint_create_enum.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
