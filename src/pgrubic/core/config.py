"""Configuration."""

import os
import typing
import pathlib
import dataclasses

import toml
from deepmerge import always_merger

from pgrubic import PACKAGE_NAME
from pgrubic.core import errors
from pgrubic.core.logger import logger

CONFIG_FILE: typing.Final[str] = f"{PACKAGE_NAME}.toml"

DEFAULT_CONFIG: typing.Final[pathlib.Path] = (
    pathlib.Path(__file__).resolve().parent.parent / CONFIG_FILE
)

CONFIG_PATH_ENVIRONMENT_VARIABLE: typing.Final[str] = (
    f"{PACKAGE_NAME.upper()}_CONFIG_PATH"
)


@dataclasses.dataclass(kw_only=True, frozen=True)
class DisallowedSchema:
    """Representation of disallowed schema."""

    name: str
    reason: str
    use_instead: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class DisallowedDataType:
    """Representation of disallowed data type."""

    name: str
    reason: str
    use_instead: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Column:
    """Representation of column."""

    name: str
    data_type: str


@dataclasses.dataclass(kw_only=True)
class Lint:
    """Representation of lint config."""

    select: list[str]
    ignore: list[str]
    include: list[str]
    exclude: list[str]
    ignore_noqa: bool
    allowed_extensions: list[str]
    allowed_languages: list[str]
    required_columns: list[Column]
    disallowed_schemas: list[DisallowedSchema]
    disallowed_data_types: list[DisallowedDataType]

    fix: bool

    timestamp_column_suffix: str
    date_column_suffix: str
    regex_partition: str
    regex_index: str
    regex_constraint_primary_key: str
    regex_constraint_unique_key: str
    regex_constraint_foreign_key: str
    regex_constraint_check: str
    regex_constraint_exclusion: str
    regex_sequence: str


@dataclasses.dataclass(kw_only=True)
class Format:
    """Representation of format config."""

    include: list[str]
    exclude: list[str]
    comma_at_beginning: bool
    new_line_before_semicolon: bool
    lines_between_statements: int
    remove_pg_catalog_from_functions: bool
    diff: bool
    check: bool


@dataclasses.dataclass(kw_only=True)
class Config:
    """Representation of config."""

    cache_dir: pathlib.Path

    include: list[str]
    exclude: list[str]

    postgres_target_version: int

    lint: Lint
    format: Format


def _load_default_config() -> dict[str, typing.Any]:
    """Load default config."""
    return dict(toml.load(DEFAULT_CONFIG))


def _load_user_config() -> dict[str, typing.Any]:
    """Load config from absolute path config file."""
    config_file_absolute_path = _get_config_file_absolute_path()

    if config_file_absolute_path:
        return dict(toml.load(config_file_absolute_path))

    return {}  # pragma: no cover


def _merge_config() -> dict[str, typing.Any]:
    """Merge default and user config."""
    return dict(always_merger.merge(_load_default_config(), _load_user_config()))


def _get_config_file_absolute_path(
    config_file: str = CONFIG_FILE,
) -> pathlib.Path | None:
    """Get the absolute path of the config file.
    If CONFIG_PATH_ENVIRONMENT_VARIABLE environment variable is set, we try to use that
    else, we use the first config file that we find upwards from the current working
    directory.
    """
    env_config_path = os.getenv(CONFIG_PATH_ENVIRONMENT_VARIABLE)

    if env_config_path:
        config_file_absolute_path = pathlib.Path(env_config_path).resolve() / config_file
        if pathlib.Path.exists(config_file_absolute_path):
            logger.info(
                """Using settings from "%s\"""",
                config_file_absolute_path,
            )
            return config_file_absolute_path

    current_directory = pathlib.Path.cwd()

    # Traverse upwards through the directory tree
    while current_directory != current_directory.parent:
        # Check if the configuration file exists
        config_file_absolute_path = current_directory / config_file

        if pathlib.Path.exists(config_file_absolute_path):
            logger.info(
                """Using settings from "%s\"""",
                config_file_absolute_path,
            )
            return config_file_absolute_path

        # Move up one directory
        current_directory = current_directory.parent  # pragma: no cover

    logger.info(
        """Using default settings""",
    )

    return None  # pragma: no cover


def parse_config() -> Config:
    """Parse config."""
    merged_config = _merge_config()
    config_lint = merged_config["lint"]
    config_format = merged_config["format"]

    try:
        return Config(
            cache_dir=pathlib.Path(merged_config["cache-dir"]),
            include=merged_config["include"],
            exclude=merged_config["exclude"],
            postgres_target_version=merged_config["target-postgres-version"],
            lint=Lint(
                select=config_lint["select"],
                ignore=config_lint["ignore"],
                include=config_lint["include"] or merged_config["include"],
                exclude=config_lint["exclude"] or merged_config["exclude"],
                ignore_noqa=config_lint["ignore-noqa"],
                allowed_extensions=config_lint["allowed-extensions"],
                allowed_languages=config_lint["allowed-languages"],
                fix=config_lint["fix"],
                timestamp_column_suffix=config_lint["timestamp-column-suffix"],
                date_column_suffix=config_lint["date-column-suffix"],
                regex_partition=config_lint["regex-partition"],
                regex_index=config_lint["regex-index"],
                regex_constraint_primary_key=config_lint["regex-constraint-primary-key"],
                regex_constraint_unique_key=config_lint["regex-constraint-unique-key"],
                regex_constraint_foreign_key=config_lint["regex-constraint-foreign-key"],
                regex_constraint_check=config_lint["regex-constraint-check"],
                regex_constraint_exclusion=config_lint["regex-constraint-exclusion"],
                regex_sequence=config_lint["regex-sequence"],
                required_columns=[
                    Column(
                        name=column["name"],
                        data_type=column["data-type"],
                    )
                    for column in config_lint["required-columns"]
                ],
                disallowed_data_types=[
                    DisallowedDataType(
                        name=data_type["name"],
                        reason=data_type["reason"],
                        use_instead=data_type["use-instead"],
                    )
                    for data_type in config_lint["disallowed-data-types"]
                ],
                disallowed_schemas=[
                    DisallowedSchema(
                        name=schema["name"],
                        reason=schema["reason"],
                        use_instead=schema["use-instead"],
                    )
                    for schema in config_lint["disallowed-schemas"]
                ],
            ),
            format=Format(
                include=config_format["include"] or merged_config["include"],
                exclude=config_format["exclude"] or merged_config["exclude"],
                comma_at_beginning=config_format["comma-at-beginning"],
                new_line_before_semicolon=config_format["new-line-before-semicolon"],
                lines_between_statements=config_format["lines-between-statements"],
                remove_pg_catalog_from_functions=config_format[
                    "remove-pg-catalog-from-functions"
                ],
                diff=config_format["diff"],
                check=config_format["check"],
            ),
        )
    except KeyError as error:
        msg = "Missing config key: "
        raise errors.MissingConfigError(msg + error.args[0]) from error
