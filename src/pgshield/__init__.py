"""pgshield."""

import pathlib

POSTGRES_MAX_IDENTIFIER: int = 63

SCHEMA_QUALIFIED_TYPE: int = 2

RULE_DIRECTORIES: list[str] = [
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
    "pgshield.rules.convention.typing",
    "pgshield.rules.convention.partitioning",
    "pgshield.rules.convention.constraint",
]

CONFIG_FILE: str = "pgshield.toml"

DEFAULT_CONFIG: pathlib.Path = pathlib.Path(__file__).resolve().parent / CONFIG_FILE

# Map system type name to generic one
varchar = "pg_catalog.varchar"

system_types = {
    "boolean": "pg_catalog.bool",
    "char": "pg_catalog.bpchar",
    "real": "pg_catalog.float4",
    "double precision": "pg_catalog.float8",
    "smallint": "pg_catalog.int2",
    "integer": "pg_catalog.int4",
    "bigint": "pg_catalog.int8",
    "interval": "pg_catalog.interval",
    "numeric": "pg_catalog.numeric",
    "time": "pg_catalog.time",
    "timestamp": "pg_catalog.timestamp",
    "timestamp with time zone": "pg_catalog.timestamptz",
    "time with time zone": "pg_catalog.timetz",
    "bit varying": "pg_catalog.varbit",
    "varchar": varchar,

    "pg_catalog.bool": "pg_catalog.bool",
    "pg_catalog.bpchar": "pg_catalog.bpchar",
    "pg_catalog.float4": "pg_catalog.float4",
    "pg_catalog.float8": "pg_catalog.float8",
    "pg_catalog.int2": "pg_catalog.int2",
    "pg_catalog.int4": "pg_catalog.int4",
    "pg_catalog.int8": "pg_catalog.int8",
    "pg_catalog.interval": "pg_catalog.interval",
    "pg_catalog.numeric": "pg_catalog.numeric",
    "pg_catalog.time": "pg_catalog.time",
    "pg_catalog.timestamp": "pg_catalog.timestamp",
    "pg_catalog.timestamptz": "pg_catalog.timestamptz",
    "pg_catalog.timetz": "pg_catalog.timetz",
    "pg_catalog.varbit": "pg_catalog.varbit",
    "pg_catalog.varchar": varchar,
}
