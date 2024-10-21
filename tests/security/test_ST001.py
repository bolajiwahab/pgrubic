"""Test extension whitelist."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.security.ST001 import ExtensionWhitelist


@pytest.fixture(scope="module")
def extension_whitelist() -> core.BaseChecker:
    """Create an instance of extension whitelist."""
    core.add_set_locations_to_rule(ExtensionWhitelist)
    return ExtensionWhitelist()


@pytest.fixture
def lint_extension_whitelist(
    linter: core.Linter,
    extension_whitelist: core.BaseChecker,
) -> core.Linter:
    """Lint extension whitelist."""
    extension_whitelist.config.lint.allowed_extensions = [
        "pg_stat_statements",
    ]
    linter.checkers.add(extension_whitelist)

    return linter


def test_extension_whitelist_rule_code(
    extension_whitelist: core.BaseChecker,
) -> None:
    """Test extension whitelist rule code."""
    assert extension_whitelist.code == extension_whitelist.__module__.split(".")[-1]


def test_extension_whitelist_auto_fixable(
    extension_whitelist: core.BaseChecker,
) -> None:
    """Test extension whitelist auto fixable."""
    assert extension_whitelist.is_auto_fixable is False


def test_pass_allowed_extension(
    lint_extension_whitelist: core.Linter,
) -> None:
    """Test pass allowed extension."""
    sql_fail: str = "CREATE EXTENSION pg_stat_statements;"

    violations: core.ViolationMetric = lint_extension_whitelist.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_extension_whitelist(
    lint_extension_whitelist: core.Linter,
) -> None:
    """Test fail extension whitelist."""
    sql_fail: str = "CREATE EXTENSION logical_ddl;"

    violations: core.ViolationMetric = lint_extension_whitelist.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_extension_whitelist_description(
    lint_extension_whitelist: core.Linter,
    extension_whitelist: core.BaseChecker,
) -> None:
    """Test extension whitelist description."""
    sql_fail: str = "CREATE EXTENSION logical_ddl;"

    _: core.ViolationMetric = lint_extension_whitelist.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(extension_whitelist.violations),
        ).description
        == "Extension 'logical_ddl' is not allowed"
    )


def test_pass_noqa_extension_whitelist(
    lint_extension_whitelist: core.Linter,
) -> None:
    """Test pass noqa extension whitelist."""
    sql_pass_noqa: str = """
    -- noqa: ST001
    CREATE EXTENSION logical_ddl;
    """

    violations: core.ViolationMetric = lint_extension_whitelist.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_extension_whitelist(
    lint_extension_whitelist: core.Linter,
) -> None:
    """Test fail noqa extension whitelist."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE EXTENSION logical_ddl;
    """

    violations: core.ViolationMetric = lint_extension_whitelist.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_extension_whitelist(
    lint_extension_whitelist: core.Linter,
) -> None:
    """Test pass noqa extension whitelist."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE EXTENSION logical_ddl;
    """

    violations: core.ViolationMetric = lint_extension_whitelist.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
