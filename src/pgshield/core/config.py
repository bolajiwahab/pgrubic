"""Load config."""

import typing
import pathlib
import dataclasses

import toml

from pgshield import CONFIG_FILE, DEFAULT_CONFIG
from pgshield.core import errors


@dataclasses.dataclass(kw_only=True, frozen=True)
class DisallowedSchema:
    """Representation of disallowed schema."""

    name: str
    reason: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class DisallowedType:
    """Representation of disallowed type."""

    name: str
    reason: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class RequiredColumns:
    """Representation of required columns."""

    name: str
    data_type: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Config:
    """Representation of config."""

    select: list[str]
    ignore: list[str]
    include: list[str]
    exclude: list[str]
    allowed_extensions: list[str]
    allowed_languages: list[str]
    partition_strategies: list[str]
    required_columns: list[RequiredColumns]
    not_null_columns: list[str]
    disallowed_schemas: list[DisallowedSchema]
    disallowed_data_types: list[DisallowedType]

    fix: bool
    unsafe_fixes: bool

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
    return dict(toml.load(DEFAULT_CONFIG))


def load_user_config() -> dict[str, typing.Any]:
    """Load config from from absolute path config file."""
    absolute_path_config_file = _get_absolute_path_config_file(CONFIG_FILE)

    if absolute_path_config_file:

        return dict(toml.load(absolute_path_config_file))

    return {}


def _merge_config() -> dict[str, typing.Any]:
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

        config = _merge_config().get("lint", {})

        lint_config = Config(
            select=config["select"],
            ignore=config["ignore"],
            include=config["include"],
            exclude=config["exclude"],
            allowed_extensions=config["allowed_extensions"],
            allowed_languages=config["allowed_languages"],
            partition_strategies=config["partition_strategies"],
            not_null_columns=config["not_null_columns"],
            fix=config["fix"],
            unsafe_fixes=config["unsafe_fixes"],
            regex_partition=config["regex_partition"],
            regex_index=config["regex_index"],
            regex_constraint_primary_key=config["regex_constraint_primary_key"],
            regex_constraint_unique_key=config["regex_constraint_unique_key"],
            regex_constraint_foreign_key=config["regex_constraint_foreign_key"],
            regex_constraint_check=config["regex_constraint_check"],
            regex_constraint_exclusion=config["regex_constraint_exclusion"],
            regex_sequence=config["regex_sequence"],
            required_columns=[
                RequiredColumns(
                    name=column["name"],
                    data_type=column["data_type"],
                )
                for column in config["required_columns"]
            ],
            disallowed_data_types=[
                DisallowedType(
                    name=data_type["name"],
                    reason=data_type["reason"],
                )
                for data_type in config["disallowed_data_types"]
            ],
            disallowed_schemas=[
                DisallowedSchema(
                    name=schema["name"],
                    reason=schema["reason"],
                )
                for schema in config["disallowed_schemas"]
            ],
        )

    except KeyError as error:

        raise errors.ConfigMissingKeyError(error.args[0]) from None

    return lint_config
