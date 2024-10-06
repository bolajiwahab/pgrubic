"""Test missing primary key."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.general.GN004 import MissingPrimaryKey


@pytest.fixture(scope="module")
def missing_primary_key() -> core.BaseChecker:
    """Create an instance of MissingPrimaryKey."""
    core.add_set_locations_to_rule(MissingPrimaryKey)
    return MissingPrimaryKey()


@pytest.fixture
def lint_missing_primary_key(
    linter: core.Linter,
    missing_primary_key: core.BaseChecker,
) -> core.Linter:
    """Lint MissingPrimaryKey."""
    linter.checkers.add(missing_primary_key)

    return linter


def test_missing_primary_key_rule_code(
    missing_primary_key: core.BaseChecker,
) -> None:
    """Test missing primary key rule code."""
    assert missing_primary_key.code == missing_primary_key.__module__.split(".")[-1]


def test_missing_primary_key_auto_fixable(
    missing_primary_key: core.BaseChecker,
) -> None:
    """Test missing primary key auto fixable."""
    assert missing_primary_key.is_auto_fixable is False


def test_pass_inline_primary_key(
    lint_missing_primary_key: core.Linter,
) -> None:
    """Test fail missing primary key."""
    sql_fail: str = "CREATE TABLE music (age int PRIMARY KEY);"

    violations: core.ViolationMetric = lint_missing_primary_key.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_standalone_primary_key(
    lint_missing_primary_key: core.Linter,
) -> None:
    """Test fail missing primary key."""
    sql_fail: str = (
        "CREATE TABLE music (age int, CONSTRAINT music_pkey PRIMARY KEY (age));"
    )

    violations: core.ViolationMetric = lint_missing_primary_key.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_missing_primary_key(
    lint_missing_primary_key: core.Linter,
) -> None:
    """Test fail missing primary key."""
    sql_fail: str = "CREATE TABLE music (age int);"

    violations: core.ViolationMetric = lint_missing_primary_key.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_missing_primary_key_description(
    lint_missing_primary_key: core.Linter,
    missing_primary_key: core.BaseChecker,
) -> None:
    """Test missing primary key description."""
    sql_fail: str = "CREATE TABLE music (age int);"

    _: core.ViolationMetric = lint_missing_primary_key.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(missing_primary_key.violations),
        ).description
        == "Table `music` missing a primary key"
    )


def test_pass_noqa_missing_primary_key(
    lint_missing_primary_key: core.Linter,
) -> None:
    """Test pass noqa missing primary key."""
    sql_pass_noqa: str = """
    -- noqa: GN004
    CREATE TABLE music (age int);
    """

    violations: core.ViolationMetric = lint_missing_primary_key.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_missing_primary_key(
    lint_missing_primary_key: core.Linter,
) -> None:
    """Test fail noqa missing primary key."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TABLE music (age int);
    """

    violations: core.ViolationMetric = lint_missing_primary_key.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_missing_primary_key(
    lint_missing_primary_key: core.Linter,
) -> None:
    """Test fail noqa missing primary key."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE TABLE music (age int);
    """

    violations: core.ViolationMetric = lint_missing_primary_key.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
