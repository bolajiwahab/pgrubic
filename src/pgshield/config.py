"""Load config from a file."""
import os
import typing
import pathlib
import configparser
import dataclasses

file_path = pathlib.Path(__file__).resolve().parent

file_name: pathlib.Path = pathlib.Path(file_path) / ".pgshield"


@dataclasses.dataclass(kw_only=True, frozen=True)
class Rules:
    """Representation of rules."""

    select: list[str] = dataclasses.field(default_factory=list)
    ignore: list[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass(kw_only=True, frozen=True)
class Convention:
    """Representation of convention."""

    schemas: list[str]


@dataclasses.dataclass(kw_only=True, frozen=True)
class Config:
    """Representation of config."""

    rules: Rules
    convention: Convention


def load_config(file_name: os.PathLike[str]) -> Config:
    """Read config from a file."""
    config = configparser.ConfigParser(delimiters="=")

    try:

        config.read(file_name, encoding="utf-8")

    except configparser.DuplicateOptionError:

        config.read(file_name, encoding="utf-8")

    # return json.loads(config.items("pgshield"))
    select = config.get("lint.select", fallback="")
    config = Config(
        rules=Rules(
            select=[rule.strip() for rule in select.split(',')],
            select=config.get("lint.rules.select", "").split(","),
            ignore=config.get("lint.rules.ignore", "").split(","),
        ),
        convention=Convention(
            schemas=config.get("lint.convention.schemas", "").split(",")
        ),
    )
    return Config(**dict(config.items("pgshield")))
    # return dict(config.items("pgshield"))
