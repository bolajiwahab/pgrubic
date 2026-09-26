"""Test cli."""

import os
import typing
import pathlib
from unittest.mock import patch

import click
import pytest
from click import testing

from tests import TEST_FILE, conftest
from pgrubic import WORKERS_ENVIRONMENT_VARIABLE
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


@pytest.mark.parametrize(
    "args",
    [
        pytest.param(["-v"], id="root-short"),
        pytest.param(["--version"], id="root-long"),
        pytest.param(["lint", "-v"], id="lint-short"),
        pytest.param(["lint", "--version"], id="lint-long"),
        pytest.param(["format", "-v"], id="format-short"),
        pytest.param(["format", "--version"], id="format-long"),
    ],
)
def test_cli_version_option(args: list[str]) -> None:
    """Test version options on the root command and subcommands."""
    result = testing.CliRunner().invoke(cli, args)

    assert result.exit_code == 0
    assert " version " in result.output


@pytest.mark.parametrize(
    ("test_command", "test_id", "test_case"),
    conftest.load_test_cases(
        test_case_type=conftest.TestCaseType.CLI,
        path=pathlib.Path("tests/fixtures/cli"),
    ),
)
def test_cli_source_file(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
    test_command: str,
    test_id: str,
    test_case: dict[str, typing.Any],
) -> None:
    """Test data-driven CLI behavior."""
    runner = testing.CliRunner()

    directory = tmp_path / "sub"
    directory.mkdir()
    monkeypatch.chdir(directory)

    config_file = directory / config.CONFIG_FILE

    if "config" in test_case:
        config_file.write_text(test_case["config"])

    source_file = directory / TEST_FILE
    source_file.write_text(test_case["sql"])

    result = runner.invoke(
        cli,
        [test_command.lower(), str(source_file), *test_case.get("args", [])],
    )

    output = click.unstyle(result.output)

    if "expected_output" in test_case:
        expected_output = test_case["expected_output"].replace(
            "{config_file}",
            str(config_file),
        )
        assert output == expected_output, (
            f"Unexpected CLI output: `{test_command}` in `{test_id}`"
        )

    if "expected_output_contains" in test_case:
        assert test_case["expected_output_contains"] in output, (
            f"Missing CLI output: `{test_command}` in `{test_id}`"
        )

    if "expected_source_code" in test_case:
        assert source_file.read_text() == test_case["expected_source_code"], (
            f"Unexpected source code: `{test_command}` in `{test_id}`"
        )

    assert result.exit_code == test_case["expected_exit_code"]


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


def test_cli_lint_with_generate_lint_report(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test the CLI generates a lint report."""
    runner = testing.CliRunner()

    directory = tmp_path / "sub"
    directory.mkdir()
    monkeypatch.chdir(directory)

    source_file = directory / TEST_FILE
    source_file.write_text("SELECT a = NULL;")

    result = runner.invoke(
        cli,
        ["lint", str(source_file), "--generate-lint-report"],
    )

    assert result.exit_code == 1
    assert (directory / linter.DEFAULT_LINT_REPORT_FILE).is_file()


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


def test_cli_format_files(tmp_path: pathlib.Path) -> None:
    """Test cli format source files."""
    runner = testing.CliRunner()

    source_code: str = f"select a = null;{noqa.NEW_LINE}"

    directory = tmp_path / "sub"
    directory.mkdir()

    source_1 = directory / "source_1.sql"
    source_1.write_text(source_code)

    source_2 = directory / "source_2.sql"
    source_2.write_text(source_code)

    source_3 = directory / "source_3.sql"
    source_3.write_text(source_code)

    result = runner.invoke(
        cli,
        [
            "format",
            str(source_1),
            str(source_2),
            "--config",
            "format.uppercase-keywords = true",
        ],
    )

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


def test_cli_format_directory(tmp_path: pathlib.Path) -> None:
    """Test cli format directory."""
    runner = testing.CliRunner()

    sql_pass: str = f"select a = null;{noqa.NEW_LINE}"

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

    # without cache read: forces reprocessing, but the file is already correctly
    # formatted by now, so nothing actually changes on disk. Set the mtime to a
    # deliberately old, unambiguous value first: comparing two "now"-ish samples
    # could false-negative on filesystems with coarse mtime resolution, where a
    # real rewrite could land in the same tick as the pre-run sample.
    old_mtime_ns = 0
    os.utime(file_fail, ns=(old_mtime_ns, old_mtime_ns))

    result = runner.invoke(cli, ["format", str(file_fail), "--no-cache"])

    assert (
        result.output
        == f"{noqa.NEW_LINE}0 file(s) reformatted, 1 file(s) left unchanged{noqa.NEW_LINE}"  # noqa: E501
    )

    assert result.exit_code == 0
    assert file_fail.stat().st_mtime_ns == old_mtime_ns


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
