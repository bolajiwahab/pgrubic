"""Test cli."""

import pathlib

import pytest
from click import testing

from tests import TEST_FILE
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


def test_cli_lint_no_specified_paths(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test cli lint no specified paths."""
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


def test_cli_format_file(tmp_path: pathlib.Path) -> None:
    """Test cli format file."""
    runner = testing.CliRunner()

    sql_pass: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_pass = directory / TEST_FILE
    file_pass.write_text(sql_pass)

    result = runner.invoke(cli, ["format", str(file_pass)])

    assert result.exit_code == 0


def test_cli_format_directory(tmp_path: pathlib.Path) -> None:
    """Test cli format directory."""
    runner = testing.CliRunner()

    sql_pass: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_pass = directory / TEST_FILE
    file_pass.write_text(sql_pass)

    result = runner.invoke(cli, ["format", str(directory)])

    assert result.exit_code == 0


def test_cli_format_no_specified_paths(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test cli format no specified paths."""
    runner = testing.CliRunner()

    sql_pass: str = "SELECT a = NULL; SELECT * FROM example;"

    directory = tmp_path / "sub"
    directory.mkdir()
    monkeypatch.chdir(directory)

    file_pass = directory / TEST_FILE
    file_pass.write_text(sql_pass)

    result = runner.invoke(cli, ["format"])

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