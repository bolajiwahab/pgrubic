"""Filters."""

import fnmatch
import pathlib


def filter_sources(
    *,
    sources: tuple[pathlib.Path, ...],
    include: list[str],
    exclude: list[str],
    extension: str = "sql",
) -> set[pathlib.Path]:
    """Filter sources base on include and exclude."""
    flattened_sources: set[pathlib.Path] = set()

    for source in sources:
        if source.is_dir():
            flattened_sources.update(source.glob(f"**/*.{extension}"))

        elif source.suffix == f".{extension}":
            flattened_sources.add(source)

    included_sources: set[pathlib.Path] = set()

    for source in flattened_sources:
        if (
            _is_file_included(
                source=str(source),
                include=include,
                exclude=exclude,
            )
            and source.stat().st_size > 0
        ):
            included_sources.add(source)

    return included_sources


def _is_file_included(
    *,
    source: str,
    include: list[str],
    exclude: list[str],
) -> bool:
    """Check if a source should be included or excluded based on global config."""
    return bool(
        (not include or any(fnmatch.fnmatch(source, pattern) for pattern in include))
        and not any(fnmatch.fnmatch(source, pattern) for pattern in exclude),
    )
