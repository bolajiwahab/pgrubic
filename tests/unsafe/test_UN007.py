"""Test drop tablespace."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.unsafe.UN007 import DropTablespace


@pytest.fixture(scope="module")
def drop_tablespace() -> core.BaseChecker:
    """Create an instance of DropTablespace."""
    return DropTablespace()


@pytest.fixture
def lint_drop_tablespace(
    linter: core.Linter,
    drop_tablespace: core.BaseChecker,
) -> core.Linter:
    """Lint DropTablespace."""
    linter.checkers.add(drop_tablespace)

    return linter


def test_drop_tablespace_rule_code(drop_tablespace: core.BaseChecker) -> None:
    """Test drop tablespace rule code."""
    assert drop_tablespace.code == drop_tablespace.__module__.split(".")[-1]


def test_drop_tablespace_auto_fixable(drop_tablespace: core.BaseChecker) -> None:
    """Test drop tablespace auto fixable."""
    assert drop_tablespace.is_auto_fixable is False


def test_fail_drop_tablespace(lint_drop_tablespace: core.Linter) -> None:
    """Test fail drop tablespace."""
    sql_fail: str = """
    DROP TABLESPACE test
    ;
    """

    violations: core.ViolationMetric = lint_drop_tablespace.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_drop_tablespace_description(
    lint_drop_tablespace: core.Linter,
    drop_tablespace: core.BaseChecker,
) -> None:
    """Test fail drop tablespace description."""
    sql_fail: str = """
    DROP TABLESPACE test
    ;
    """

    _: core.ViolationMetric = lint_drop_tablespace.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(iter(drop_tablespace.violations)).description == "Drop tablespace detected"
    )


def test_pass_noqa_drop_tablespace(lint_drop_tablespace: core.Linter) -> None:
    """Test pass noqa tablespace column."""
    sql_pass_noqa: str = """
    DROP TABLESPACE test -- noqa: UN007
    ;
    """

    violations: core.ViolationMetric = lint_drop_tablespace.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_drop_tablespace(lint_drop_tablespace: core.Linter) -> None:
    """Test fail noqa drop tablespace."""
    sql_noqa: str = """
    DROP TABLESPACE test -- noqa: UN002
    ;
    """

    violations: core.ViolationMetric = lint_drop_tablespace.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_drop_tablespace(
    lint_drop_tablespace: core.Linter,
) -> None:
    """Test fail noqa drop tablespace."""
    sql_noqa: str = """
    DROP TABLESPACE test -- noqa:
    ;
    """

    violations: core.ViolationMetric = lint_drop_tablespace.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
