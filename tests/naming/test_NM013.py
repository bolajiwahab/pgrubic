"""Test pg prefix identifier."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.naming.NM013 import PgPrefixIdentifier


@pytest.fixture(scope="module")
def pg_prefix_identifier() -> core.BaseChecker:
    """Create an instance of pg prefix identifier."""
    core.add_set_locations_to_rule(PgPrefixIdentifier)
    return PgPrefixIdentifier()


@pytest.fixture
def lint_pg_prefix_identifier(
    linter: core.Linter,
    pg_prefix_identifier: core.BaseChecker,
) -> core.Linter:
    """Lint pg prefix identifier."""
    linter.checkers.add(pg_prefix_identifier)

    return linter


def test_pg_prefix_identifier_rule_code(
    pg_prefix_identifier: core.BaseChecker,
) -> None:
    """Test pg prefix identifier rule code."""
    assert pg_prefix_identifier.code == pg_prefix_identifier.__module__.split(".")[-1]


def test_pg_prefix_identifier_auto_fixable(
    pg_prefix_identifier: core.BaseChecker,
) -> None:
    """Test pg prefix identifier auto fixable."""
    assert pg_prefix_identifier.is_auto_fixable is False


def test_fail_pg_prefix_identifier(
    lint_pg_prefix_identifier: core.Linter,
) -> None:
    """Test fail pg prefix identifier."""
    sql_fail: str = (
        "CREATE TABLE tbl (id int, CONSTRAINT pg_tbl_pkey PRIMARY KEY (id));"
    )

    violations: core.ViolationMetric = lint_pg_prefix_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_pg_prefix_identifier_description(
    lint_pg_prefix_identifier: core.Linter,
    pg_prefix_identifier: core.BaseChecker,
) -> None:
    """Test pg prefix identifier description."""
    sql_fail: str = "CREATE ROLE pg_notify_me LOGIN;"

    _: core.ViolationMetric = lint_pg_prefix_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(pg_prefix_identifier.violations),
        ).description
        == "Identifier should not use prefix `pg_`"
    )


def test_pass_noqa_pg_prefix_identifier(
    lint_pg_prefix_identifier: core.Linter,
) -> None:
    """Test pass noqa pg prefix identifier."""
    sql_pass_noqa: str = """
    -- noqa: NM013
    CREATE TYPE pg_complex AS (
        r       double precision,
        i       double precision
    );
    """

    violations: core.ViolationMetric = lint_pg_prefix_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_pg_prefix_identifier(
    lint_pg_prefix_identifier: core.Linter,
) -> None:
    """Test fail noqa pg prefix identifier."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE tbl (id int, CONSTRAINT pg_tbl_pkey PRIMARY KEY (id))
    """

    violations: core.ViolationMetric = lint_pg_prefix_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_pg_prefix_identifier(
    lint_pg_prefix_identifier: core.Linter,
) -> None:
    """Test pass noqa pg prefix identifier."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE pg_tbl (id int, CONSTRAINT tbl_pkey PRIMARY KEY (id))
    """

    violations: core.ViolationMetric = lint_pg_prefix_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
