"""Test linter."""

import typing
import pathlib

import pytest

from tests import conftest
from pgrubic import DOCUMENTATION_URL, RULE_DOCUMENTATION_BASE, core

SOURCE_FILE = "linter.sql"


@pytest.mark.parametrize(
    ("test_linter", "test_id", "test_case"),
    conftest.load_test_cases(
        test_case_type=conftest.TestCaseType.CORE,
        path=pathlib.Path("tests/fixtures/core/linter.yml"),
    ),
)
def test_linter(
    linter: core.Linter,
    test_linter: str,
    test_id: str,
    test_case: dict[str, typing.Any],
) -> None:
    """Test linter behavior."""
    config_overrides = typing.cast(
        dict[str, typing.Any],
        test_case.get("config", {}),
    )

    with conftest.update_config(config=linter.config, overrides=config_overrides):
        result = linter.run(
            source_file=SOURCE_FILE,
            source_code=test_case["sql"],
        )

    assert len(result.violations) == test_case["expected_violation_count"], (
        f"Unexpected violations: `{test_linter}` in `{test_id}`"
    )
    expected_errors = set(test_case.get("expected_errors", []))
    expected_error_count = test_case.get(
        "expected_error_count",
        len(expected_errors),
    )
    assert len(result.errors) == expected_error_count, (
        f"Unexpected error count: `{test_linter}` in `{test_id}`"
    )
    if expected_errors:
        assert {error.message for error in result.errors} == expected_errors, (
            f"Unexpected errors: `{test_linter}` in `{test_id}`"
        )

    if "expected_fixed_source_code" in test_case:
        assert result.fixed_source_code == test_case["expected_fixed_source_code"], (
            f"Unexpected fixed source: `{test_linter}` in `{test_id}`"
        )


def test_linter_generate_lint_report(
    linter: core.Linter,
    tmp_path: pathlib.Path,
) -> None:
    """Test linter lint report."""
    directory = tmp_path / "sub"
    directory.mkdir()
    report_file = directory / "report.md"

    # The ordering of violations is not guaranteed
    # So we only check for one violation here
    lint_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="SELECT a = NULL; SELECT b FROM;",
    )

    linter.generate_lint_report(
        lint_results=[lint_result],
        report_file=str(report_file),
    )

    expected_lint_report = f"""## Pgrubic Lint Report

Total violations: **1**

Total errors: **1**

<details>
<summary>Violations (1)</summary>

| File | Line | Col | Rule | Description | Help |
|------|------|-----|------|-------------|------|
| linter.sql | 1 | 10 | [GN024]({DOCUMENTATION_URL}/{RULE_DOCUMENTATION_BASE}/general/null-comparison) | Comparison with NULL should be [IS | IS NOT] NULL | Use [IS | IS NOT] NULL |
</details>

<details>
<summary>Errors (1)</summary>

| File | Message | Hint |
|------|---------|------|
| linter.sql | syntax error at or near ";", at index 14 | Make sure the statement is valid PostgreSQL statement. If it is, please report this issue at https://github.com/bolajiwahab/pgrubic/issues |
</details>
"""  # noqa: E501

    assert report_file.read_text() == expected_lint_report
