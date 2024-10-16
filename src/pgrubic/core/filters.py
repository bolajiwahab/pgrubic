"""Filters."""

import fnmatch
import pathlib

from pgrubic.core import config


def filter_files(
    *,
    paths: tuple[pathlib.Path, ...],
    config: config.Config,
) -> tuple[pathlib.Path, ...]:
    """Filters files base on config.lint.include and config.lint.exclude."""
    source_files: set[pathlib.Path] = set()

    for path in paths:
        if path.is_dir():
            source_files.update(path.glob("**/*.sql"))

        else:
            source_files.add(path)

    return tuple(
        source_file
        for source_file in source_files
        if is_file_included(source_file=str(source_file), config=config)
        and source_file.stat().st_size > 0
    )


def is_file_included(*, source_file: str, config: config.Config) -> bool:
    """Check if a source_file should be included or excluded based on global config."""
    return bool(
        (
            not config.lint.include
            or any(
                fnmatch.fnmatch(source_file, pattern) for pattern in config.lint.include
            )
        )
        and not any(
            fnmatch.fnmatch(source_file, pattern) for pattern in config.lint.exclude
        ),
    )
