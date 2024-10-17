"""Filters."""

import fnmatch
import pathlib


def filter_files(
    *,
    paths: tuple[pathlib.Path, ...],
    include: list[str],
    exclude: list[str],
    extension: str = "sql",
) -> tuple[pathlib.Path, ...]:
    """Filters files base on include and exclude."""
    source_files: set[pathlib.Path] = set()

    for path in paths:
        if path.is_dir():
            source_files.update(path.glob(f"**/*.{extension}"))

        elif path.suffix == f".{extension}":
            source_files.add(path)

    return tuple(
        source_file
        for source_file in source_files
        if _is_file_included(
            source_file=str(source_file),
            include=include,
            exclude=exclude,
        )
        and source_file.stat().st_size > 0
    )


def _is_file_included(
    *,
    source_file: str,
    include: list[str],
    exclude: list[str],
) -> bool:
    """Check if a source_file should be included or excluded based on global config."""
    return bool(
        (not include or any(fnmatch.fnmatch(source_file, pattern) for pattern in include))
        and not any(fnmatch.fnmatch(source_file, pattern) for pattern in exclude),
    )
