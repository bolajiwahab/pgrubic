"""Test entry."""

import pathlib

from click import testing

from tests import TEST_FILE
from pgrubic import core
from pgrubic.__main__ import cli


def test_cli(tmp_path: pathlib.Path, linter: core.Linter) -> None:
    """CLI."""
    runner = testing.CliRunner()
    linter.config.lint.fix = False

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / TEST_FILE
    file_fail.write_text(sql_fail)

    result = runner.invoke(cli, ["lint", str(file_fail)])

    assert result.exit_code == 1

    linter.config.lint.fix = True

    result = runner.invoke(cli, ["lint", str(file_fail)])

    assert result.exit_code == 1
