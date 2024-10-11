"""Test entry."""

import pathlib

from click import testing

from tests import TEST_FILE
from pgrubic.__main__ import cli


def test_cli_file(tmp_path: pathlib.Path) -> None:
    """CLI."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail)])

    assert result.exit_code == 1


def test_cli_directory(tmp_path: pathlib.Path) -> None:
    """CLI."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(directory)])

    assert result.exit_code == 1


def test_cli_complete_fix(tmp_path: pathlib.Path) -> None:
    """CLI."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail), "--fix"])

    assert result.exit_code == 0


def test_cli_partial_fix(tmp_path: pathlib.Path) -> None:
    """CLI."""
    runner = testing.CliRunner()

    sql_fail: str = "SELECT a = NULL; SELECT * FROM example;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail), "--fix"])

    assert result.exit_code == 1
