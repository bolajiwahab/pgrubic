"""Test keyword identifier."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.naming.NM011 import KeywordIdentifier


@pytest.fixture(scope="module")
def keyword_identifier() -> core.BaseChecker:
    """Create an instance of keyword identifier."""
    core.add_set_locations_to_rule(KeywordIdentifier)
    return KeywordIdentifier()


@pytest.fixture
def lint_keyword_identifier(
    linter: core.Linter,
    keyword_identifier: core.BaseChecker,
) -> core.Linter:
    """Lint keyword identifier."""
    linter.checkers.add(keyword_identifier)

    return linter


def test_keyword_identifier_rule_code(
    keyword_identifier: core.BaseChecker,
) -> None:
    """Test keyword identifier rule code."""
    assert keyword_identifier.code == keyword_identifier.__module__.split(".")[-1]


def test_keyword_identifier_auto_fixable(
    keyword_identifier: core.BaseChecker,
) -> None:
    """Test keyword identifier  auto fixable."""
    assert keyword_identifier.is_auto_fixable is False


def test_fail_keyword_identifier(
    lint_keyword_identifier: core.Linter,
) -> None:
    """Test fail keyword identifier."""
    sql_fail: str = """CREATE SEQUENCE "TABLE" START 1;"""

    violations: core.ViolationMetric = lint_keyword_identifier.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_keyword_identifier_description(
    lint_keyword_identifier: core.Linter,
    keyword_identifier: core.BaseChecker,
) -> None:
    """Test keyword identifier description."""
    sql_fail: str = """CREATE TABLESPACE "TABLESPACE" LOCATION 'directory_path';"""

    _: core.ViolationMetric = lint_keyword_identifier.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(keyword_identifier.violations),
        ).description
        == "Keyword `TABLESPACE` used as an identifier"
    )


def test_pass_noqa_keyword_identifier(
    lint_keyword_identifier: core.Linter,
) -> None:
    """Test pass noqa keyword identifier."""
    sql_pass_noqa: str = """
    -- noqa: NM011
    CREATE SCHEMA "SCHEMA";
    """

    violations: core.ViolationMetric = lint_keyword_identifier.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_keyword_identifier(
    lint_keyword_identifier: core.Linter,
) -> None:
    """Test fail noqa keyword identifier."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE DATABASE "DATABASE";
    """

    violations: core.ViolationMetric = lint_keyword_identifier.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_keyword_identifier(
    lint_keyword_identifier: core.Linter,
) -> None:
    """Test pass noqa keyword identifier."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE INDEX "INDEX" ON tbl (col);
    """

    violations: core.ViolationMetric = lint_keyword_identifier.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
