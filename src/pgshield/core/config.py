"""Load config."""

import typing
import pathlib
import dataclasses

import toml  # type: ignore[import-untyped]

from pgshield import config_file, default_config
from pgshield.core import errors


@dataclasses.dataclass(kw_only=True, frozen=True)
class Config:
    """Representation of config."""

    select: list[str] = dataclasses.field(default_factory=list)
    ignore: list[str] = dataclasses.field(default_factory=list)
    schemas: list[str] = dataclasses.field(default_factory=list)
    extensions: list[str] = dataclasses.field(default_factory=list)
    regex_partition: str = (
        "[a-zA-Z0-9]+__[a-zA-Z0-9]+__[0-9]{4}_[0-9]{2}(?:_[0-9]{2})?$"
    )
    regex_index: str = "[a-zA-Z0-9]+_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_idx$"
    regex_unique_index: str = "[a-zA-Z0-9]+_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_key$"

    regex_constraint_primary_key: str = "[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_key$"
    regex_constraint_unique_key: str = (
        "[a-zA-Z0-9]+_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_key$"
    )
    regex_constraint_foreign_key: str = (
        "[a-zA-Z0-9]+_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_fkey"
    )
    regex_constraint_check: str = "[a-zA-Z0-9]+_[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*_check$"


def _load_default_config() -> dict[str, typing.Any]:
    """Load default config."""
    return dict(toml.load(default_config))


def _load_user_config() -> dict[str, typing.Any]:
    """Load config from from absolute path config file."""
    absolute_path_config_file = _get_absolute_path_config_file(config_file)

    if absolute_path_config_file:

        return dict(toml.load(absolute_path_config_file))

    return dict(toml.load(default_config))


def _merge_config() -> dict[str, typing.Any]:
    """Merge default and user config."""
    return {k: v | _load_user_config()[k] for k, v in _load_default_config().items()}


def _get_absolute_path_config_file(config_file: str) -> pathlib.Path | None:
    """Get the absolute path of the config file. We use the first config file we find upwards."""  # noqa: E501
    current_directory = pathlib.Path.cwd()

    # Traverse upwards through the directory tree
    while current_directory != current_directory.parent:

        # Check if the configuration file exists
        config_absolute_path = current_directory / config_file

        if pathlib.Path.exists(config_absolute_path):
            return config_absolute_path

        # Move up one directory
        current_directory = current_directory.parent

    return None


def parse_config() -> Config:
    """Parse config."""
    try:
        config = Config(**_merge_config().get("lint", {}))

    except TypeError as error:

        raise errors.UnexpectedConfigDetectedError(error.args[0]) from error

    return config
