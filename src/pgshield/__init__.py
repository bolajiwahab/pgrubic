"""pgshield."""

import re
import pathlib

POSTGRES_MAX_IDENTIFIER: int = 63

rule_directories: list[str] = [
    "pgshield.rules.unsafe.table",
    "pgshield.rules.unsafe.column",
    "pgshield.rules.unsafe.index",
    "pgshield.rules.unsafe.constraint",
    "pgshield.rules.unsafe.storage",
    "pgshield.rules.convention.naming",
    "pgshield.rules.convention.schema",
    "pgshield.rules.convention.identifier",
    "pgshield.rules.convention.extension",
    "pgshield.rules.convention.general",
]

config_file: str = "pgshield.toml"

default_config: pathlib.Path = pathlib.Path(__file__).resolve().parent / config_file


def recover_original_identifier(sql: str, identifier: str) -> str:
    """Postgres truncates identifiers to 63 characters at parse time, same goes for pglast."""  # noqa: E501
    match = list(set(re.findall(r"\b" + re.escape(identifier) + r"\S*\b", sql)))

    return str(match[0])
