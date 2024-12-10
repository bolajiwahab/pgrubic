"""Test filters."""

import pathlib

from pgrubic import core


def test_filter_lint_sources(tmp_path: pathlib.Path, linter: core.Linter) -> None:
    """Test filter lint sources."""
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

    sources: tuple[pathlib.Path, ...] = (
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

    for source in sources:
        file_fail = directory / source
        file_fail.write_text(sql_fail)

    sources_filtered_length = 9

    sources_to_be_formatted = core.filter_sources(
        sources=(directory,),
        include=linter.config.lint.include,
        exclude=linter.config.lint.exclude,
    )

    assert len(sources_to_be_formatted) == sources_filtered_length


def test_filter_format_sources(tmp_path: pathlib.Path, linter: core.Linter) -> None:
    """Test filter format sources."""
    linter.config.format.include = [
        "*.sql",
        "*.txt",
    ]

    linter.config.format.exclude = [
        "test.sql",
    ]

    sql_fail: str = "SELECT a = NULL;"

    directory = tmp_path / "sub"
    directory.mkdir()

    sources: tuple[pathlib.Path, ...] = (
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

    for path in sources:
        file_fail = directory / path
        file_fail.write_text(sql_fail)

    sources_filtered_length = 9

    sources_to_be_formatted = core.filter_sources(
        sources=(directory,),
        include=linter.config.format.include,
        exclude=linter.config.format.exclude,
    )

    assert len(sources_to_be_formatted) == sources_filtered_length
