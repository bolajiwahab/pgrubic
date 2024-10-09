"""Test entry."""

import pathlib

import pytest

from tests import SOURCE_PATH
from pgrubic import PROGRAM_NAME, core, __main__


def test_cli(tmp_path: pathlib.Path, linter: core.Linter) -> None:
    """CLI."""
    linter.config.lint.fix = False

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    file_fail = directory / SOURCE_PATH
    file_fail.write_text(sql_fail)

    args = [PROGRAM_NAME, str(file_fail)]
    with pytest.raises(SystemExit) as excinfo:
        __main__.cli(argv=args)

    assert excinfo.value.code == 1

    linter.config.lint.fix = True
    with pytest.raises(SystemExit) as excinfo:
        __main__.cli(argv=args)

    assert excinfo.value.code == 1
