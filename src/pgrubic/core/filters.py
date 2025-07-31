"""Filters."""

import fnmatch
import pathlib


def filter_sources(
    *,
    sources: tuple[pathlib.Path, ...],
    include: list[str],
    exclude: list[str],
    respect_gitignore: bool,
    extension: str = "sql",
) -> set[pathlib.Path]:
    """Filter sources base on include and exclude and either respect gitignore.

    Paramaters:
    -----------
    sources: tuple[pathlib.Path, ...]
        List of sources to filter.
    include: list[str]
        List of file patterns to include.
    exclude: list[str]
        List of file patterns to exclude.
    respect_gitignore: bool
        Whether to respect gitignore.
    extension: str
        File extension to filter. Default is "sql".

    Returns:
    -------
    set[pathlib.Path]
        Set of filtered sources.

    """
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
            if respect_gitignore and _is_git_ignored(str(source)):
                continue

            included_sources.add(source)

    return included_sources


def _is_file_included(
    *,
    source: str,
    include: list[str],
    exclude: list[str],
) -> bool:
    """Check if a source should be included or excluded based on global config.

    Paramaters:
    -----------
    source: str
        Path to the source file.
    include: list[str]
        List of file patterns to include.
    exclude: list[str]
        List of file patterns to exclude.

    Returns:
    -------
    bool
        True if the source should be included, False otherwise.

    """
    return bool(
        (not include or any(fnmatch.fnmatch(source, pattern) for pattern in include))
        and not any(fnmatch.fnmatch(source, pattern) for pattern in exclude),
    )


def _is_git_ignored(source: str) -> bool:
    """Check if a source is git ignored.

    Parameters:
    -----------
    source: str
        Path to the source file.

    Returns:
    -------
    bool
        True if the source is git ignored, False otherwise.

    """
    try:
        # git needs to be installed for us to be able to check if a file is git ignored
        import git  # noqa: PLC0415
        import git.exc  # noqa: PLC0415

        repo = git.Repo(source, search_parent_directories=True)
        return bool(repo.ignored(source))
    except ImportError:  # pragma: no cover
        # git is not installed
        return False
    except (git.exc.InvalidGitRepositoryError, git.exc.GitCommandError):
        return False
