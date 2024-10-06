"""Test filters."""

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

    source_paths = [
        "test.sql",
        "test.py",
        "test.txt",
        "tables.sql",
        "views.sql",
        "functions.sql",
        "triggers.sql",
        "rules.sql",
        "procedures.sql",
        "types.sql",
        "alters.sql",
    ]

    source_paths_filtered_length = 9

    source_paths = core.filter_source_paths(
        source_paths=source_paths,
        config=linter.config,
    )

    assert len(source_paths) == source_paths_filtered_length
