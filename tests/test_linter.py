"""Test linter."""

import pathlib

from pgrubic import core
from pgrubic.core import noqa

SOURCE_FILE = "linter.sql"


def test_linter_violations(
    linter: core.Linter,
) -> None:
    """Test linter violations."""
    linting_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="SELECT a = NULL, 10 = b;",
    )

    expected_number_of_violations: int = 2

    assert len(linting_result.violations) == expected_number_of_violations


def test_linter_suppressed_all_violations(
    linter: core.Linter,
) -> None:
    """Test linter suppressed all violations."""
    linting_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="""
        -- noqa
        SELECT a = NULL, 10 = b;
        """,
    )

    assert len(linting_result.violations) == 0


def test_linter_suppressed_certain_violations(
    linter: core.Linter,
) -> None:
    """Test linter suppressed certain violations."""
    linting_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="""
        -- noqa: GN024
        SELECT a = NULL, 10 = b;
        """,
    )

    assert len(linting_result.violations) == 1


def test_linter_violations_fixed_source_code(
    linter: core.Linter,
) -> None:
    """Test linter fixed sql."""
    linter.config.lint.fix = True
    linting_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="""
SELECT a = NULL;
SELECT b IS NULL;
""",
    )

    assert (
        linting_result.fixed_source_code
        == f"SELECT a IS NULL;{noqa.NEW_LINE}{noqa.NEW_LINE}SELECT b IS NULL;{noqa.NEW_LINE}"  # noqa: E501
    )


def test_linter_violations_no_fixed_source_code(
    linter: core.Linter,
) -> None:
    """Test linter no fixed sql."""
    linter.config.lint.fix = False
    linting_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="""SELECT a = NULL;

        SELECT b = NULL;
        """,
    )

    assert not linting_result.fixed_source_code


def test_linter_suppressed_violations_fixed_source_code(
    linter: core.Linter,
) -> None:
    """Test linter suppressed violations fixed sql."""
    linter.config.lint.fix = True
    linting_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="""-- noqa: GN024
SELECT a = NULL;
""",
    )

    assert not linting_result.fixed_source_code


def test_lint_parse_error(linter: core.Linter) -> None:
    """Test parse error."""
    source_code: str = "CREATE TABLE tbl (activated);"

    linting_result = linter.run(
        source_file=SOURCE_FILE,
        source_code=source_code,
    )

    assert len(linting_result.errors) == 1


def test_new_line_before_semicolon(
    linter: core.Linter,
) -> None:
    """Test new line before semicolon."""
    linter.config.lint.fix = True
    linter.config.format.new_line_before_semicolon = True
    linting_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="SELECT a = NULL;",
    )

    linter.config.format.new_line_before_semicolon = False

    assert (
        linting_result.fixed_source_code
        == f"SELECT a IS NULL{noqa.NEW_LINE};{noqa.NEW_LINE}"
    )


def test_fix_enablement(
    linter: core.Linter,
) -> None:
    """Test fix enablement."""
    linter.config.lint.fix = True
    linter.config.lint.fixable = ["GN024"]
    linting_result = linter.run(
        source_file=SOURCE_FILE,
        source_code="SELECT a = NULL;",
    )

    assert linting_result.fixed_source_code == f"SELECT a IS NULL;{noqa.NEW_LINE}"


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

    expected_lint_report = """## Pgrubic Lint Report

Total violations: **1**

Total errors: **1**

<details>
<summary>Violations (1)</summary>

| File | Line | Col | Rule | Description | Help |
|------|------|-----|------|-------------|------|
| linter.sql | 1 | 10 | [GN024](https://bolajiwahab.github.io/pgrubic/rules/general/null-comparison) | Comparison with NULL should be [IS | IS NOT] NULL | Use [IS | IS NOT] NULL |
</details>

<details>
<summary>Errors (1)</summary>

| File | Message | Hint |
|------|---------|------|
| linter.sql | syntax error at or near ";", at index 13 | Make sure the statement is valid PostgreSQL statement. If it is, please report this issue at https://github.com/bolajiwahab/pgrubic/issues
 |
</details>
"""  # noqa: E501

    assert report_file.read_text() == expected_lint_report
