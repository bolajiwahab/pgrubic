"""Test filters."""

import pathlib

from pgrubic import core


def test_filter_source_paths(linter: core.Linter) -> None:
    """Test filtering source paths."""
    linter.config.lint.include = [
        "*.sql",
        "*.txt",
    ]

    linter.config.lint.exclude = [
        "test.sql",
    ]

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

    source_paths_filtered_length = 9

    paths = core.filter_files(
        paths=paths,
        config=linter.config,
    )

    assert len(paths) == source_paths_filtered_length
