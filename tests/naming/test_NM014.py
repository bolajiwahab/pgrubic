"""Test single letter identifier."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.naming.NM014 import SingleLetterIdentifier


@pytest.fixture(scope="module")
def single_letter_identifier() -> core.BaseChecker:
    """Create an instance of single letter identifier."""
    core.add_set_locations_to_rule(SingleLetterIdentifier)
    return SingleLetterIdentifier()


@pytest.fixture
def lint_single_letter_identifier(
    linter: core.Linter,
    single_letter_identifier: core.BaseChecker,
) -> core.Linter:
    """Lint single letter identifier."""
    linter.checkers.add(single_letter_identifier)

    return linter


def test_single_letter_identifier_rule_code(
    single_letter_identifier: core.BaseChecker,
) -> None:
    """Test single letter identifier rule code."""
    assert (
        single_letter_identifier.code
        == single_letter_identifier.__module__.split(".")[-1]
    )


def test_single_letter_identifier_auto_fixable(
    single_letter_identifier: core.BaseChecker,
) -> None:
    """Test single letter identifier auto fixable."""
    assert single_letter_identifier.is_auto_fixable is False


def test_fail_single_letter_identifier(
    lint_single_letter_identifier: core.Linter,
) -> None:
    """Test fail single letter identifier."""
    sql_fail: str = "CREATE TABLE tbl (a int);"

    violations: core.ViolationMetric = lint_single_letter_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_single_letter_identifier_description(
    lint_single_letter_identifier: core.Linter,
    single_letter_identifier: core.BaseChecker,
) -> None:
    """Test single letter identifier description."""
    sql_fail: str = "CREATE ROLE b LOGIN;"

    _: core.ViolationMetric = lint_single_letter_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(single_letter_identifier.violations),
        ).description
        == "Single letter identifier `b` is not descriptive enough"
    )


def test_pass_noqa_single_letter_identifier(
    lint_single_letter_identifier: core.Linter,
) -> None:
    """Test pass noqa single letter identifier."""
    sql_pass_noqa: str = """
    -- noqa: NM014
    CREATE TABLE b (age int);
    """

    violations: core.ViolationMetric = lint_single_letter_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_single_letter_identifier(
    lint_single_letter_identifier: core.Linter,
) -> None:
    """Test fail noqa single letter identifier."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN a int;
    """

    violations: core.ViolationMetric = lint_single_letter_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_single_letter_identifier(
    lint_single_letter_identifier: core.Linter,
) -> None:
    """Test pass noqa single letter identifier."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE tbl (age int, CONSTRAINT a PRIMARY KEY (id))
    """

    violations: core.ViolationMetric = lint_single_letter_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
