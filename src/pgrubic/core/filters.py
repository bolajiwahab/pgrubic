"""Filters."""

import fnmatch
from collections import abc

from pgrubic.core import config


def filter_source_paths(
    *,
    source_paths: abc.Sequence[str],
    config: config.Config,
) -> list[str]:
    """Filters source paths based on config.include and config.exclude."""
    return [
        source_path
        for source_path in source_paths
        if is_source_path_included(source_path, config)
    ]


def is_source_path_included(source_path: str, config: config.Config) -> bool:
    """Check if a file should be included or excluded based on global config."""
    return bool(
        (
            not config.lint.include
            or any(
                fnmatch.fnmatch(source_path, pattern) for pattern in config.lint.include
            )
        )
        and not any(
            fnmatch.fnmatch(source_path, pattern) for pattern in config.lint.exclude
        ),
    )
