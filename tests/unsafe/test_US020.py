"""Test non concurrent index reindex."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.unsafe.US020 import NonConcurrentReindex


@pytest.fixture(scope="module")
def non_concurrent_reindex() -> core.BaseChecker:
    """Create an instance of NonConcurrentReindex."""
    core.add_apply_fix_to_rule(NonConcurrentReindex)
    core.add_set_locations_to_rule(NonConcurrentReindex)
    return NonConcurrentReindex()


@pytest.fixture
def lint_non_concurrent_reindex(
    linter: core.Linter,
    non_concurrent_reindex: core.BaseChecker,
) -> core.Linter:
    """Lint NonConcurrentReindex."""
    non_concurrent_reindex.config.lint.fix = False
    linter.checkers.add(non_concurrent_reindex)

    return linter


def test_non_concurrent_reindex_rule_code(
    non_concurrent_reindex: core.BaseChecker,
) -> None:
    """Test non concurrent index reindex rule code."""
    assert (
        non_concurrent_reindex.code
        == non_concurrent_reindex.__module__.split(
            ".",
        )[-1]
    )


def test_non_concurrent_reindex_auto_fixable(
    non_concurrent_reindex: core.BaseChecker,
) -> None:
    """Test non concurrent index reindex auto fixable."""
    assert non_concurrent_reindex.is_auto_fixable is True


def test_pass_concurrent_reindex(
    lint_non_concurrent_reindex: core.Linter,
) -> None:
    """Test pass concurrent reindex."""
    sql_pass: str = "REINDEX INDEX CONCURRENTLY idx;"

    violations: core.ViolationMetric = lint_non_concurrent_reindex.run(
        source_file=TEST_FILE,
        source_code=sql_pass,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_reindex(
    lint_non_concurrent_reindex: core.Linter,
) -> None:
    """Test non concurrent index reindex."""
    sql_fail: str = "REINDEX INDEX idx;"

    violations: core.ViolationMetric = lint_non_concurrent_reindex.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_non_concurrent_reindex_description(
    lint_non_concurrent_reindex: core.Linter,
    non_concurrent_reindex: core.BaseChecker,
) -> None:
    """Test non concurrent index reindex description."""
    sql_fail: str = "REINDEX TABLE tbl;"

    _: core.ViolationMetric = lint_non_concurrent_reindex.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(non_concurrent_reindex.violations),
        ).description
        == "Non concurrent reindex"
    )


def test_pass_noqa_non_concurrent_reindex(
    lint_non_concurrent_reindex: core.Linter,
) -> None:
    """Test pass noqa non concurrent index reindex."""
    sql_pass_noqa: str = """
    -- noqa: US020
    REINDEX DATABASE db;
    """

    violations: core.ViolationMetric = lint_non_concurrent_reindex.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_non_concurrent_reindex(
    lint_non_concurrent_reindex: core.Linter,
) -> None:
    """Test fail noqa non concurrent index reindex."""
    sql_noqa: str = """
    -- noqa: US001
    REINDEX SCHEMA schm;
    """

    violations: core.ViolationMetric = lint_non_concurrent_reindex.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_non_concurrent_reindex(
    lint_non_concurrent_reindex: core.Linter,
) -> None:
    """Test pass noqa non concurrent index reindex."""
    sql_noqa: str = """
    -- noqa
    REINDEX INDEX idx;
    """

    violations: core.ViolationMetric = lint_non_concurrent_reindex.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_non_concurrent_reindex(
    lint_non_concurrent_reindex: core.Linter,
    non_concurrent_reindex: core.BaseChecker,
) -> None:
    """Test fail fix non concurrent index reindex."""
    sql_fail: str = "REINDEX INDEX idx;"

    sql_fix: str = "REINDEX (CONCURRENTLY) INDEX idx;\n"

    non_concurrent_reindex.config.lint.fix = True

    violations: core.ViolationMetric = lint_non_concurrent_reindex.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
