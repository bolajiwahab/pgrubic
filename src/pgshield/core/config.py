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

    select: list[str]
    ignore: list[str]
    include: list[str]
    exclude: list[str]
    schemas: list[str]
    extensions: list[str]
    partition_strategies: list[str]
    required_columns: dict[str, str]
    not_null_columns: list[str]
    blacklisted_types: list[str]

    regex_partition: str
    regex_index: str
    regex_constraint_primary_key: str
    regex_constraint_unique_key: str
    regex_constraint_foreign_key: str
    regex_constraint_check: str
    regex_constraint_exclusion: str

    regex_sequence: str


def load_default_config() -> dict[str, typing.Any]:
    """Load default config."""
    return dict(toml.load(default_config))


def load_user_config() -> dict[str, typing.Any]:
    """Load config from from absolute path config file."""
    absolute_path_config_file = _get_absolute_path_config_file(config_file)

    if absolute_path_config_file:

        return dict(toml.load(absolute_path_config_file))

    return {}


def merge_config() -> dict[str, typing.Any]:
    """Merge default and user config."""
    return {
        k: v | load_user_config().get(k, {}) for k, v in load_default_config().items()
    }


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
        config = Config(**merge_config().get("lint", {}))

    except TypeError as error:

        raise errors.UnexpectedConfigDetectedError(error.args[0]) from error

    return config
