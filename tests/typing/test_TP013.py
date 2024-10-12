"""Test usage of hstore."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.typing.TP013 import Hstore


@pytest.fixture(scope="module")
def hstore() -> core.BaseChecker:
    """Create an instance of hstore."""
    core.add_apply_fix_to_rule(Hstore)
    core.add_set_locations_to_rule(Hstore)
    return Hstore()


@pytest.fixture
def lint_hstore(
    linter: core.Linter,
    hstore: core.BaseChecker,
) -> core.Linter:
    """Lint hstore."""
    hstore.config.lint.fix = False
    linter.checkers.add(hstore)

    return linter


def test_hstore_rule_code(
    hstore: core.BaseChecker,
) -> None:
    """Test hstore rule code."""
    assert hstore.code == hstore.__module__.split(".")[-1]


def test_hstore_auto_fixable(
    hstore: core.BaseChecker,
) -> None:
    """Test hstore auto fixable."""
    assert hstore.is_auto_fixable is True


def test_pass_create_table_hstore(
    lint_hstore: core.Linter,
) -> None:
    """Test pass jsonb."""
    sql_fail: str = "CREATE TABLE tbl (details jsonb);"

    violations: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_hstoreb(
    lint_hstore: core.Linter,
) -> None:
    """Test pass jsonb."""
    sql_fail: str = """
    ALTER TABLE tbl ADD COLUMN details jsonb;
    """

    violations: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_hstore(
    lint_hstore: core.Linter,
) -> None:
    """Test fail create table hstore."""
    sql_fail: str = "CREATE TABLE tbl (details hstore);"

    violations: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_hstore(
    lint_hstore: core.Linter,
) -> None:
    """Test fail alter table hstore."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN details hstore;"

    violations: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_hstore_description(
    lint_hstore: core.Linter,
    hstore: core.BaseChecker,
) -> None:
    """Test hstore description."""
    sql_fail: str = "CREATE TABLE tbl (details hstore);"

    _: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(hstore.violations),
        ).description
        == "Prefer jsonb over hstore"
    )


def test_pass_noqa_hstore(
    lint_hstore: core.Linter,
) -> None:
    """Test pass noqa hstore."""
    sql_pass_noqa: str = """
    -- noqa: TP013
    CREATE TABLE tbl (tbl_id int, details hstore)
    """

    violations: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_hstore(
    lint_hstore: core.Linter,
) -> None:
    """Test fail noqa hstore."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN details hstore;
    """

    violations: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_hstore(
    lint_hstore: core.Linter,
) -> None:
    """Test pass noqa hstore."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE tbl (tbl_id int, details hstore);
    """

    violations: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_hstore(
    lint_hstore: core.Linter,
    hstore: core.BaseChecker,
) -> None:
    """Test fail fix hstore."""
    sql_fail: str = "CREATE TABLE tbl (user_id int, details hstore);"

    sql_fix: str = "CREATE TABLE tbl (\n    user_id integer\n  , details jsonb\n);"

    hstore.config.lint.fix = True

    violations: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_hstore(
    lint_hstore: core.Linter,
    hstore: core.BaseChecker,
) -> None:
    """Test fail fix hstore."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN details hstore;"

    sql_fix: str = "ALTER TABLE tbl\n    ADD COLUMN details jsonb;"

    hstore.config.lint.fix = True

    violations: core.ViolationMetric = lint_hstore.run(
        file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
