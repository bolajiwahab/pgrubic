"""Test filters."""

import pathlib

from pgrubic import core


def test_filter_source_paths(tmp_path: pathlib.Path, linter: core.Linter) -> None:
    """Test filtering source paths."""
    linter.config.lint.include = [
        "*.sql",
        "*.txt",
    ]

    linter.config.lint.exclude = [
        "test.sql",
    ]

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    paths: tuple[pathlib.Path, ...] = (
        pathlib.Path("test.sql"),
        pathlib.Path("test.py"),
        pathlib.Path("test.txt"),
        pathlib.Path("tables.sql"),
        pathlib.Path("views.sql"),
        pathlib.Path("functions.sql"),
        pathlib.Path("triggers.sql"),
        pathlib.Path("rules.sql"),
        pathlib.Path("procedures.sql"),
        pathlib.Path("types.sql"),
        pathlib.Path("alters.sql"),
    )

    for path in paths:
        file_fail = directory / path
        file_fail.write_text(sql_fail)

    source_paths_filtered_length = 9

    paths = core.filter_files(
        paths=(directory,),
        include=linter.config.lint.include,
        exclude=linter.config.lint.exclude,
    )

    assert len(paths) == source_paths_filtered_length
