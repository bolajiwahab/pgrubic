"""Test cli."""

import pathlib
from unittest.mock import patch

import click
import pytest
from click import testing

from tests import TEST_FILE
from pgrubic import (
    DOCUMENTATION_URL,
    RULE_DOCUMENTATION_BASE,
    WORKERS_ENVIRONMENT_VARIABLE,
)
from pgrubic.core import noqa, config, linter
from pgrubic.__main__ import cli


@pytest.mark.parametrize(
    ("args", "description", "usage_command"),
    [
        (["--help"], "Pgrubic: A PostgreSQL linter", "cli"),
        (
            ["lint", "--help"],
            "Run the SQL linter on the given files or directories.",
            "cli lint",
        ),
    ],
)
def test_cli_help_colors(
    args: list[str],
    description: str,
    usage_command: str,
) -> None:
    """Test help colors are emitted only when color output is enabled."""
    runner = testing.CliRunner()

    colored_result = runner.invoke(cli, args, color=True)
    plain_result = runner.invoke(cli, args)

    assert colored_result.exit_code == 0
    assert "\x1b[" in colored_result.output
    assert click.style(usage_command, fg="green", bold=True) in colored_result.output
    assert plain_result.exit_code == 0
    assert "\x1b[" not in plain_result.output
    assert plain_result.output.index(description) < plain_result.output.index("Usage:")
    assert "Parameters:" not in plain_result.output
    assert '--config "lint.target-postgres-version = 17"' in plain_result.output
    if args == ["lint", "--help"]:
        normalized_output = " ".join(plain_result.output.split())
        assert "Ignore inline `-- noqa` directives." in normalized_output
        assert "causing the entire file to be ignored by the linter." in normalized_output
    if args == ["--help"]:
        assert plain_result.output.index("\nCommands:\n") < plain_result.output.index(
            "\nOptions:\n",
        )
        assert "\nConfiguration overrides:\n" in plain_result.output
        assert "\nExamples:\n" in plain_result.output


@pytest.mark.parametrize("args", [["-v"], ["lint", "-v"]])
def test_cli_short_version_option(args: list[str]) -> None:
    """Test the short version option on the root and subcommands."""
    result = testing.CliRunner().invoke(cli, args)

    assert result.exit_code == 0
    assert " version " in result.output


def test_cli_lint_file(tmp_path: pathlib.Path) -> None:
    """Test cli lint file."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail)])

    assert result.exit_code == 1


def test_cli_lint_directory(tmp_path: pathlib.Path) -> None:
    """Test cli lint directory."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(directory)])

    assert result.exit_code == 1


def test_cli_lint_current_directory(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test cli lint current directory."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()
    monkeypatch.chdir(directory)

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint"])

    assert result.exit_code == 1


def test_cli_lint_complete_fix(tmp_path: pathlib.Path) -> None:
    """Test cli lint complete fix."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail), "--fix"])

    assert result.exit_code == 0


def test_cli_lint_config_override(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test overriding lint configuration from the CLI."""
    runner = testing.CliRunner()
    monkeypatch.chdir(tmp_path)
    (tmp_path / config.CONFIG_FILE).write_text(
        """
[lint]
fix = false
""",
    )
    source_file = tmp_path / TEST_FILE
    source_file.write_text("SELECT a = NULL;")

    result = runner.invoke(
        cli,
        ["lint", "--config", "lint.fix = true", str(source_file)],
    )

    assert result.exit_code == 0
    assert source_file.read_text() == f"SELECT a IS NULL;{noqa.NEW_LINE}"


def test_cli_lint_with_add_file_level_general_noqa(tmp_path: pathlib.Path) -> None:
    """Test cli lint with add_file_level_general_noqa."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail), "--add-file-level-general-noqa"])

    assert (
        result.output
        == f"File-level general noqa directive added to 1 file(s){noqa.NEW_LINE}"
    )

    assert result.exit_code == 0


def test_cli_lint_with_generate_lint_report(tmp_path: pathlib.Path) -> None:
    """Test cli lint with generate_lint_report."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()
    report_file = linter.DEFAULT_LINT_REPORT_FILE

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    runner.invoke(cli, ["lint", str(file_fail), "--generate-lint-report"])

    expected_lint_report = f"""## Pgrubic Lint Report

Total violations: **1**

Total errors: **0**

<details>
<summary>Violations (1)</summary>

| File | Line | Col | Rule | Description | Help |
|------|------|-----|------|-------------|------|
| test.sql | 1 | 10 | [GN024]({DOCUMENTATION_URL}/{RULE_DOCUMENTATION_BASE}/general/null-comparison) | Comparison with NULL should be [IS | IS NOT] NULL | Use [IS | IS NOT] NULL |
</details>
"""  # noqa: E501

    assert pathlib.Path(report_file).read_text() == expected_lint_report

    runner.invoke(cli, ["lint", str(file_fail), "--generate-lint-report"])

    assert pathlib.Path(report_file).read_text() == expected_lint_report


def test_cli_lint_no_violations(tmp_path: pathlib.Path) -> None:
    """Test cli lint with add_file_level_general_noqa."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail)])

    assert result.output == f"All checks passed!{noqa.NEW_LINE}"

    assert result.exit_code == 0


def test_cli_lint_verbose(tmp_path: pathlib.Path) -> None:
    """Test cli lint verbose."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail), "--verbose"])

    assert result.exit_code == 1


def test_cli_lint_partial_fix(tmp_path: pathlib.Path) -> None:
    """Test cli lint partial fix."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL; SELECT * FROM example;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail), "--fix"])

    assert result.exit_code == 1


def test_cli_lint_ignore_noqa(tmp_path: pathlib.Path) -> None:
    """Test cli lint ignore noqa."""
    runner = testing.CliRunner()

    sql_fail: str = """
    -- noqa: GN024
    SELECT a = NULL;
    """

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail), "--ignore-noqa"])

    assert result.exit_code == 1


def test_cli_lint_parse_error(tmp_path: pathlib.Path) -> None:
    """Test cli lint parse error."""
    runner = testing.CliRunner()

    sql: str = "CREATE TABLE tbl (activated);"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    result = runner.invoke(cli, ["lint", str(file_fail)])

    assert result.exit_code == 1


def test_cli_lint_missing_config_error(tmp_path: pathlib.Path) -> None:
    """Test cli lint missing config error."""
    config_content = """
    [lint]
    required-columns = [
        { name = "foo", type = "text" }
    ]
    """
    runner = testing.CliRunner()

    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    sql: str = "CREATE TABLE tbl (activated);"

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    with patch("os.getcwd", return_value=str(directory)):
        result = runner.invoke(cli, ["lint", str(file_fail)])

        assert result.output == f"""Missing config key: data-type{noqa.NEW_LINE}"""
        assert result.exit_code == 1


@pytest.mark.parametrize("command", ["lint", "format"])
def test_cli_invalid_type_casting_style_error(
    command: str,
    tmp_path: pathlib.Path,
) -> None:
    """Test CLI invalid config value errors."""
    config_content = """
    [format]
    type-casting-style = "invalid"
    """
    directory = tmp_path / "sub"
    directory.mkdir()
    (directory / config.CONFIG_FILE).write_text(config_content)

    source_file = directory / TEST_FILE
    source_file.write_text("SELECT 1;")

    runner = testing.CliRunner()
    with patch("os.getcwd", return_value=str(directory)):
        result = runner.invoke(cli, [command, str(source_file)])

    assert result.output == (
        'Invalid config value for key "format.type-casting-style": "invalid". '
        'Expected one of: "native", "standard", "literal"'
        f"{noqa.NEW_LINE}"
    )
    assert result.exit_code == 1


def test_cli_lint_config_file_from_environment_variable_not_found_error(
    tmp_path: pathlib.Path,
) -> None:
    """Test cli lint config file from environment variable not found error."""
    runner = testing.CliRunner()

    directory = tmp_path / "sub"
    directory.mkdir()

    sql: str = "CREATE TABLE tbl (activated);"

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    with patch.dict(
        "os.environ",
        {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: "directory"},
    ):
        result = runner.invoke(cli, ["lint", str(file_fail)])

        assert (
            result.output
            == f"""Config file "pgrubic.toml" not found in the path set in the environment variable PGRUBIC_CONFIG_PATH{noqa.NEW_LINE}"""  # noqa: E501
        )

        assert result.exit_code == 1


def test_cli_lint_config_parse_error(
    tmp_path: pathlib.Path,
) -> None:
    """Test cli lint config parse error."""
    config_content = """
    [lint]
    fix =
    """
    runner = testing.CliRunner()

    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    sql: str = "CREATE TABLE tbl (activated);"

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    with patch("os.getcwd", return_value=str(directory)):
        result = runner.invoke(cli, ["lint", str(file_fail)])

        assert (
            result.output
            == f"""Error parsing configuration file "{config_file}"{noqa.NEW_LINE}"""
        )

        assert result.exit_code == 1


def test_cli_format_files(tmp_path: pathlib.Path) -> None:
    """Test cli format source files."""
    runner = testing.CliRunner()

    source_code: str = f"SELECT a = NULL;{noqa.NEW_LINE}"

    directory = tmp_path / "sub"
    directory.mkdir()

    source_1 = directory / "source_1.sql"
    source_1.write_text(source_code)

    source_2 = directory / "source_2.sql"
    source_2.write_text(source_code)

    source_3 = directory / "source_3.sql"
    source_3.write_text(source_code)

    result = runner.invoke(cli, ["format", str(source_1), str(source_2)])

    assert (
        result.output
        == f"{noqa.NEW_LINE}2 file(s) reformatted, 0 file(s) left unchanged{noqa.NEW_LINE}"  # noqa: E501
    )

    assert result.exit_code == 0

    # source_1 and source_2 are cached
    result = runner.invoke(cli, ["format", str(source_1), str(source_2)])
    assert (
        result.output
        == f"{noqa.NEW_LINE}0 file(s) reformatted, 2 file(s) left unchanged{noqa.NEW_LINE}"  # noqa: E501
    )

    assert result.exit_code == 0

    # Add a new source
    result = runner.invoke(cli, ["format", str(source_1), str(source_2), str(source_3)])
    assert (
        result.output
        == f"{noqa.NEW_LINE}1 file(s) reformatted, 2 file(s) left unchanged{noqa.NEW_LINE}"  # noqa: E501
    )

    assert result.exit_code == 0


def test_cli_format_file_verbose(tmp_path: pathlib.Path) -> None:
    """Test cli format file."""
    runner = testing.CliRunner()

    sql_pass: str = f"SELECT a = NULL;{noqa.NEW_LINE}"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_pass = directory / TEST_FILE
    file_pass.write_text(sql_pass)

    result = runner.invoke(cli, ["format", str(file_pass), "--verbose"])

    assert "Using default settings" in result.output

    assert result.exit_code == 0


def test_cli_format_directory(tmp_path: pathlib.Path) -> None:
    """Test cli format directory."""
    runner = testing.CliRunner()

    sql_pass: str = f"SELECT a = NULL;{noqa.NEW_LINE}"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_pass = directory / TEST_FILE
    file_pass.write_text(sql_pass)

    result = runner.invoke(cli, ["format", str(directory)])

    assert (
        result.output
        == f"{noqa.NEW_LINE}1 file(s) reformatted, 0 file(s) left unchanged{noqa.NEW_LINE}"  # noqa: E501
    )

    assert result.exit_code == 0


def test_cli_format_current_directory(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test cli format current directory."""
    runner = testing.CliRunner()

    sql_pass: str = "SELECT a = NULL; SELECT * FROM example;"

    directory = tmp_path / "sub"
    directory.mkdir()
    monkeypatch.chdir(directory)

    file_pass = directory / TEST_FILE
    file_pass.write_text(sql_pass)

    result = runner.invoke(cli, ["format"])

    assert (
        result.output
        == f"{noqa.NEW_LINE}1 file(s) reformatted, 0 file(s) left unchanged{noqa.NEW_LINE}"  # noqa: E501
    )

    assert result.exit_code == 0


def test_cli_format_check(tmp_path: pathlib.Path) -> None:
    """Test cli format check."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL; SELECT * FROM example;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["format", str(file_fail), "--check"])

    assert result.output == ""

    assert result.exit_code == 1


def test_cli_format_check_parse_error(tmp_path: pathlib.Path) -> None:
    """Test cli format check parse error."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a =;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["format", str(file_fail), "--check"])

    assert f"1 error(s) found{noqa.NEW_LINE}" in result.output

    assert result.exit_code == 1


def test_cli_format_diff(tmp_path: pathlib.Path) -> None:
    """Test cli format check."""
    runner = testing.CliRunner()

    sql: str = "SELECT a = NULL; SELECT * FROM example;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    result = runner.invoke(cli, ["format", str(file_fail), "--diff"])

    assert result.exit_code == 1


def test_cli_format_no_cache(tmp_path: pathlib.Path) -> None:
    """Test cli format with no cache."""
    runner = testing.CliRunner()

    sql: str = "SELECT a = NULL; SELECT * FROM example;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    result = runner.invoke(cli, ["format", str(file_fail)])

    assert (
        result.output
        == f"{noqa.NEW_LINE}1 file(s) reformatted, 0 file(s) left unchanged{noqa.NEW_LINE}"  # noqa: E501
    )

    assert result.exit_code == 0

    # with cache read
    result = runner.invoke(cli, ["format", str(file_fail)])

    assert (
        result.output
        == f"{noqa.NEW_LINE}0 file(s) reformatted, 1 file(s) left unchanged{noqa.NEW_LINE}"  # noqa: E501
    )

    assert result.exit_code == 0

    # without cache
    result = runner.invoke(cli, ["format", str(file_fail), "--no-cache"])

    assert (
        result.output
        == f"{noqa.NEW_LINE}1 file(s) reformatted, 0 file(s) left unchanged{noqa.NEW_LINE}"  # noqa: E501
    )

    assert result.exit_code == 0


def test_cli_format_parse_error(tmp_path: pathlib.Path) -> None:
    """Test cli format parse error."""
    runner = testing.CliRunner()

    sql: str = "SELECT * FROM;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    result = runner.invoke(cli, ["format", str(file_fail)])

    assert result.exit_code == 1


def test_max_workers_from_environment_variable(tmp_path: pathlib.Path) -> None:
    """Test max workers from environment variable."""
    with patch.dict(
        "os.environ",
        {WORKERS_ENVIRONMENT_VARIABLE: "1"},
    ):
        runner = testing.CliRunner()

        sql: str = "SELECT * FROM tbl;"

        directory = tmp_path / "sub"
        directory.mkdir()

        file_fail = directory / TEST_FILE
        file_fail.write_text(sql)

        result = runner.invoke(cli, ["format", str(file_fail)])

        assert result.exit_code == 0


def test_cli_format_missing_config_error(tmp_path: pathlib.Path) -> None:
    """Test cli format missing config error."""
    config_content = """
    [lint]
    required-columns = [
        { name = "foo", type = "text" }
    ]
    """
    runner = testing.CliRunner()

    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    sql: str = "CREATE TABLE tbl (activated);"

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    with patch("os.getcwd", return_value=str(directory)):
        result = runner.invoke(cli, ["format", str(file_fail)])

        assert result.output == f"Missing config key: data-type{noqa.NEW_LINE}"

        assert result.exit_code == 1


def test_cli_format_config_overrides(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test overriding multiple format options from the CLI."""
    runner = testing.CliRunner()
    monkeypatch.chdir(tmp_path)
    (tmp_path / config.CONFIG_FILE).write_text(
        """
[format]
uppercase-keywords = true
type-casting-style = "literal"
""",
    )
    source_file = tmp_path / TEST_FILE
    source_file.write_text("SELECT CAST(value AS text);")

    result = runner.invoke(
        cli,
        [
            "format",
            "--config",
            "format.uppercase-keywords = false",
            "--config",
            'format.type-casting-style = "native"',
            str(source_file),
        ],
    )

    assert result.exit_code == 0
    assert source_file.read_text() == f"select value::text;{noqa.NEW_LINE}"


@pytest.mark.parametrize("command", ["lint", "format"])
def test_cli_invalid_config_override(
    command: str,
    tmp_path: pathlib.Path,
) -> None:
    """Test invalid CLI configuration overrides."""
    runner = testing.CliRunner()
    source_file = tmp_path / TEST_FILE
    source_file.write_text("SELECT 1;")

    result = runner.invoke(
        cli,
        [command, "--config", "format.uppercase-keywords", str(source_file)],
    )

    assert result.exit_code == 1
    assert result.output == (
        f'Error parsing configuration override "format.uppercase-keywords"{noqa.NEW_LINE}'
    )


def test_cli_format_config_file_from_environment_variable_not_found_error(
    tmp_path: pathlib.Path,
) -> None:
    """Test cli format config file from environment variable not found error."""
    runner = testing.CliRunner()

    directory = tmp_path / "sub"
    directory.mkdir()

    sql: str = "CREATE TABLE tbl (activated);"

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    with patch.dict(
        "os.environ",
        {config.CONFIG_PATH_ENVIRONMENT_VARIABLE: "directory"},
    ):
        result = runner.invoke(cli, ["format", str(file_fail)])

        assert (
            result.output
            == f"""Config file "pgrubic.toml" not found in the path set in the environment variable PGRUBIC_CONFIG_PATH{noqa.NEW_LINE}"""  # noqa: E501
        )

        assert result.exit_code == 1


def test_cli_format_config_parse_error(
    tmp_path: pathlib.Path,
) -> None:
    """Test cli format config parse error."""
    config_content = """
    [format]
    lines-between-statements =
    """
    runner = testing.CliRunner()

    directory = tmp_path / "sub"
    directory.mkdir()

    config_file = directory / config.CONFIG_FILE
    config_file.write_text(config_content)

    sql: str = "CREATE TABLE tbl (activated);"

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    with patch("os.getcwd", return_value=str(directory)):
        result = runner.invoke(cli, ["format", str(file_fail)])

        assert (
            result.output
            == f"""Error parsing configuration file "{config_file}"{noqa.NEW_LINE}"""
        )

        assert result.exit_code == 1
