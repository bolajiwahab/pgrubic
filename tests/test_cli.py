"""Test cli."""

import pathlib
from unittest.mock import patch

import pytest
from click import testing

from tests import TEST_FILE
from pgrubic import MAX_WORKERS_ENVIRONMENT_VARIABLE
from pgrubic.__main__ import cli


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


def test_cli_lint_with_add_file_level_general_noqa(tmp_path: pathlib.Path) -> None:
    """Test cli lint with add_file_level_general_noqa."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail), "--add-file-level-general-noqa"])

    assert result.output == "File-level general noqa directive added to 1 file(s)\n"

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

    expected_exit_code: int = 2

    assert result.exit_code == expected_exit_code


def test_cli_format_file(tmp_path: pathlib.Path) -> None:
    """Test cli format file."""
    runner = testing.CliRunner()

    sql_pass: str = "SELECT a = NULL;\n"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_pass = directory / TEST_FILE
    file_pass.write_text(sql_pass)

    result = runner.invoke(cli, ["format", str(file_pass)])

    assert result.output == "1 file(s) reformatted, 0 file(s) left unchanged\n"

    assert result.exit_code == 0


def test_cli_format_file_verbose(tmp_path: pathlib.Path) -> None:
    """Test cli format file."""
    runner = testing.CliRunner()

    sql_pass: str = "SELECT a = NULL;\n"

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

    sql_pass: str = "SELECT a = NULL;\n"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_pass = directory / TEST_FILE
    file_pass.write_text(sql_pass)

    result = runner.invoke(cli, ["format", str(directory)])

    assert result.output == "1 file(s) reformatted, 0 file(s) left unchanged\n"

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

    assert result.output == "1 file(s) reformatted, 0 file(s) left unchanged\n"

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

    assert result.output == "1 file(s) reformatted, 0 file(s) left unchanged\n"

    assert result.exit_code == 0

    # with cache read
    result = runner.invoke(cli, ["format", str(file_fail)])

    assert result.output == "0 file(s) reformatted, 1 file(s) left unchanged\n"

    assert result.exit_code == 0

    # without cache
    result = runner.invoke(cli, ["format", str(file_fail), "--no-cache"])

    assert result.output == "1 file(s) reformatted, 0 file(s) left unchanged\n"

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

    expected_exit_code: int = 2

    assert result.exit_code == expected_exit_code


def test_cli_format_missing_terminator_error(tmp_path: pathlib.Path) -> None:
    """Test cli format missing terminator error."""
    runner = testing.CliRunner()

    sql: str = "SELECT * FROM tbl"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql)

    result = runner.invoke(cli, ["format", str(file_fail)])

    expected_exit_code: int = 2

    assert result.exit_code == expected_exit_code


def test_max_workers_from_environment_variable(tmp_path: pathlib.Path) -> None:
    """Test max workers from environment variable."""
    with patch.dict(
        "os.environ",
        {MAX_WORKERS_ENVIRONMENT_VARIABLE: "1"},
    ):
        runner = testing.CliRunner()

        sql: str = "SELECT * FROM tbl;"

        directory = tmp_path / "sub"
        directory.mkdir()

        file_fail = directory / TEST_FILE
        file_fail.write_text(sql)

        result = runner.invoke(cli, ["format", str(file_fail)])

        assert result.exit_code == 0
