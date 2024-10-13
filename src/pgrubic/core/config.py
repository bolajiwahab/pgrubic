"""Load config."""

import typing
import pathlib
import functools
import dataclasses

import toml

from pgrubic import CONFIG_FILE, DEFAULT_CONFIG


@dataclasses.dataclass(kw_only=True, frozen=True)
class DisallowedSchema:
    """Representation of disallowed schema."""

    name: str
    reason: str
    use_instead: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class DisallowedType:
    """Representation of disallowed type."""

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
    disallowed_data_types: list[DisallowedType]

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

    comma_at_eoln: bool
    semicolon_after_last_statement: bool
    separate_statements: int
    remove_pg_catalog_from_functions: bool
    diff: bool
    check: bool


@dataclasses.dataclass(kw_only=True)
class Config:
    """Representation of config."""

    lint: Lint
    format: Format


def _load_default_config() -> dict[str, typing.Any]:
    """Load default config."""
    return dict(toml.load(DEFAULT_CONFIG))


def _load_user_config() -> dict[str, typing.Any]:
    """Load config from from absolute path config file."""
    config_file_absolute_path = _get_config_file_absolute_path(CONFIG_FILE)

    if config_file_absolute_path:
        return dict(toml.load(config_file_absolute_path))

    return {}  # pragma: no cover


def _merge_config() -> dict[str, typing.Any]:
    """Merge default and user config."""
    return {
        k: v | _load_user_config().get(k, {}) for k, v in _load_default_config().items()
    }


def _get_config_file_absolute_path(config_file: str) -> pathlib.Path | None:
    """Get the absolute path of the config file.
    We use the first config file we find upwards.
    """
    current_directory = pathlib.Path.cwd()

    # Traverse upwards through the directory tree
    while current_directory != current_directory.parent:
        # Check if the configuration file exists
        config_absolute_path = current_directory / config_file

        if pathlib.Path.exists(config_absolute_path):
            return config_absolute_path

        # Move up one directory
        current_directory = current_directory.parent  # pragma: no cover

    return None  # pragma: no cover


@functools.lru_cache(maxsize=1)
def parse_config() -> Config:
    """Parse config."""
    merged_config = _merge_config()
    config_lint = merged_config["lint"]
    config_format = merged_config["format"]

    return Config(
        lint=Lint(
            select=config_lint["select"],
            ignore=config_lint["ignore"],
            include=config_lint["include"],
            exclude=config_lint["exclude"],
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
                DisallowedType(
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
            comma_at_eoln=config_format["comma-at-eoln"],
            semicolon_after_last_statement=config_format[
                "semicolon-after-last-statement"
            ],
            separate_statements=config_format["separate-statements"],
            remove_pg_catalog_from_functions=config_format[
                "remove-pg-catalog-from-functions"
            ],
            diff=config_format["diff"],
            check=config_format["check"],
        ),
    )
