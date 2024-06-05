"""pgshield."""

rules_directories: list[str] = [
    "pgshield.rules.unsafe.table",
    "pgshield.rules.unsafe.column",
    "pgshield.rules.unsafe.index",
    "pgshield.rules.unsafe.constraint",
    "pgshield.rules.unsafe.storage",
    "pgshield.rules.convention.naming",
    "pgshield.rules.convention.schema",
    "pgshield.rules.convention.identifier",
    "pgshield.rules.convention.convention",
]
