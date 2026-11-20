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

    Parameters:
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
            paths = set(source.glob(f"**/*.{extension}"))

            if respect_gitignore:
                paths -= _git_ignored(source, paths)

            flattened_sources.update(paths)

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
    """Check if a source should be included or excluded based on global config.

    Parameters:
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


def _git_ignored(directory: pathlib.Path, paths: set[pathlib.Path]) -> set[pathlib.Path]:
    """Return the paths under a directory that git ignores.

    Parameters:
    -----------
    directory: pathlib.Path
        Directory the paths were found in.
    paths: set[pathlib.Path]
        Paths to check.

    Returns:
    -------
    set[pathlib.Path]
        Paths that git ignores.

    """
    try:
        # git needs to be installed for us to be able to check if a file is git ignored
        import git  # noqa: PLC0415
        import git.exc  # noqa: PLC0415

        # Lists the ignored files under the directory, and each wholly ignored
        # directory once, such as "build/". With -z, git ends each path with NUL
        # instead of quoting names such as "café.sql".
        output = git.Git(directory).ls_files(
            "--others",
            "--ignored",
            "--exclude-standard",
            "--directory",
            "-z",
        )
    except ImportError:  # pragma: no cover
        # git is not installed
        return set()
    except git.exc.GitCommandError:
        # The directory is not in a git repository.
        return set()

    ignored = {directory / name for name in output.split("\0") if name}

    # A path is ignored when it, or a directory containing it, is listed.
    return {
        path
        for path in paths
        if path in ignored or any(parent in ignored for parent in path.parents)
    }
