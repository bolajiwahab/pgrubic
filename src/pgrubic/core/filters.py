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
    files: list[pathlib.Path] = []

    for path in paths:

        if path.is_dir():

            files.extend(path.glob("**/*.sql"))

        else:

            files.append(path)

    return tuple(
        file for file in files if is_file_included(file=str(file), config=config)
    )


def is_file_included(*, file: str, config: config.Config) -> bool:
    """Check if a file should be included or excluded based on global config."""
    return bool(
        (
            not config.lint.include
            or any(fnmatch.fnmatch(file, pattern) for pattern in config.lint.include)
        )
        and not any(fnmatch.fnmatch(file, pattern) for pattern in config.lint.exclude),
    )
