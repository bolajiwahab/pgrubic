# pgrubic

[![pgrubic](https://img.shields.io/badge/pgrubic-purple.svg)](https://github.com/bolajiwahab/pgrubic/)
[![PyPI - Version](https://img.shields.io/pypi/v/pgrubic)](https://pypi.org/project/pgrubic/)
[![PyPI - Status](https://img.shields.io/pypi/status/pgrubic)](https://pypi.org/project/pgrubic/)
[![PyPI - License](https://img.shields.io/pypi/l/pgrubic)](https://github.com/bolajiwahab/pgrubic/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pgrubic)](https://pypi.org/project/pgrubic/)
[![CI](https://github.com/bolajiwahab/pgrubic/actions/workflows/ci.yml/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/ci.yml)
[![Coverage badge](https://github.com/bolajiwahab/pgrubic/raw/python-coverage-comment-action-data/badge.svg)](https://github.com/bolajiwahab/pgrubic/tree/python-coverage-comment-action-data)
[![DOC](https://github.com/bolajiwahab/pgrubic/actions/workflows/doc.yml/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/doc.yml)
[![release](https://github.com/bolajiwahab/pgrubic/actions/workflows/release.yml/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/release.yml)
[![PyPI Total Downloads](https://img.shields.io/pepy/dt/pgrubic)](https://pepy.tech/projects/pgrubic)
[![CodeQL](https://github.com/bolajiwahab/pgrubic/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/bolajiwahab/pgrubic/actions/workflows/github-code-scanning/codeql)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff)
[![types - mypy](https://img.shields.io/badge/types-mypy-blue.svg)](https://github.com/python/mypy)

Pgrubic is a PostgreSQL linter and formatter for schema migrations and design best practices.

## Features

- Over 100+ rules
- Automatic violation correction (e.g., automatically add `concurrently` to index create statements)
- River style code formatting for DML statements
- Almost identical stying with **pg_dump** for DDL statements
- Python 3.12+ compatibility
- Automatic caching to avoid reformatting unchanged files
- Violations suppression, statement level, and file level

## Getting Started

For more, see the [documentation](https://bolajiwahab.github.io/pgrubic/).

## Installation

```bash
pip install pgrubic
```

**<span style="color:red">Pgrubic is only supported on Python 3.12 or higher</span>**.

## Usage

For linting, try any of the following:

```bash
pgrubic lint                         # Lint SQL files in the current directory (and any subdirectories)
pgrubic lint .                       # Lint SQL files in the current directory (and any subdirectories)
pgrubic lint directory               # Lint SQL files in *directory* (and any subdirectories)
pgrubic lint directory/*.sql         # Lint SQL files in *directory*
pgrubic lint directory/file.sql      # Lint `file.sql` in *directory*
pgrubic lint file.sql                # Lint `file.sql`
pgrubic lint directory/*.sql --fix   # Lint SQL files in *directory* and fix violations automatically
pgrubic lint file.sql --fix          # Lint `file.sql` and fix fixable violations automatically
```

Sample output from linting:

```bash
pgrubic lint *.sql

file.sql:1:38: TP017: Boolean field should be not be nullable

1 | ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

```bash
pgrubic file.sql

test.sql:1:38: TP017: Boolean field should be not be nullable

1 | ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

For formatting, try any of the following:

```bash
pgrubic format                         # Format SQL files in the current directory (and any subdirectories)
pgrubic format .                       # Format SQL files in the current directory (and any subdirectories)
pgrubic format directory               # Format SQL files in *directory* (and any subdirectories)
pgrubic format directory/*.sql         # Format SQL files in *directory*
pgrubic format directory/file.sql      # Format `file.sql` in *directory*
pgrubic format file.sql                # Format `file.sql`
pgrubic format directory/*.sql --check # Check if SQL files would have been modified, returning a non-zero exit code
pgrubic format file.sql --diff         # Report if `file.sql` would have been modified, returning a non-zero exit code as well the difference between `file.sql` and how the formatted file would look like
```

Pgrubic can also be used as a pre-commit hook:

```
- repo: https://github.com/bolajiwahab/pgrubic
  rev: 0.5.3
  hooks:
    - id: pgrubic-lint
    - id: pgrubic-format
```

## Configuration

Pgrubic can be configured via the [`pgrubic.toml`] file in either the current directory, up to the root directory or the path set by the `PGRUBIC_CONFIG_PATH` environment variable.

The following configuration options are available in the [`pgrubic.toml`] with the following defaults:

```toml
# Path to the cache directory
cache-dir = ".pgrubic_cache"

# Include all files by default
include = []

# Exclude no files by default
exclude = []

[lint]
# Target version 14 of PostgreSQL by default
postgres-target-version = 14

# Enable all rules by default
select = []

# Disable no rules by default
ignore = []

# Include all files by default
include = []

# Exclude no files by default
exclude = []

# Ignore suppressing violations that are marked as `noqa` by default
ignore-noqa = false

# Disallowed schemas
disallowed-schemas = []

# Allowed extensions
allowed-extensions = []

# Allowed languages
allowed-languages = []

# Do not fix violations automatically
fix = false

# Consider all rules as fixable
fixable = []

# Consider all rules as fixable
unfixable = []

# Disallowed data types
disallowed-data-types = []

# Required columns
required-columns = []

# Suffix Timestamp columns with `_at` by default
timestamp-column-suffix = "_at"

# Suffix Date columns with suffix `_date` by default
date-column-suffix = "_date"

# Allow nay naming convention for partitions by default
regex-partition = "^.+$"

# Allow all any naming convention for indexes by default
regex-index = "^.+$"

# Allow any naming convention for primary key constraints by default
regex-constraint-primary-key = "^.+$"

# ALlow any naming convention for unique keys by default
regex-constraint-unique-key = "^.+$"

# Allow any naming convention for foreign keys by default
regex-constraint-foreign-key = "^.+$"

# Allow any naming convention for check constraints by default
regex-constraint-check = "^.+$"

# Allow any naming convention for exclusion constraints by default
regex-constraint-exclusion = "^.+$"

# Allow any naming convention for sequences by default
regex-sequence = "^.+$"

[format]
# Include all files by default
include = []

# Exclude no files by default
exclude = []

# Comma at the beginning of an item by default
comma-at-beginning = true

# New line before semicolon false by default
new-line-before-semicolon = false

# Remove pg_catalog from functions by default
remove-pg-catalog-from-functions = true

# Separate statements by a certain number by of new line, 1 by default
lines-between-statements = 1

# Check if files would have been modified, returning a non-zero exit code
check = false

# Report if files would have been modified, returning a non-zero exit code as well the difference between the current file and how the formatted file would look like
diff = false

# Whether to read the cache.
no-cache = false
```

Some configuration options can be supplied via CLI arguments such as `--check`, `--diff`, `--fix`.

```bash
pgrubic format --check
```

```bash
pgrubic format --diff
```

```bash
pgrubic lint --fix
```

## Rules

There are 100+ rules. All rules are enabled by default. For a complete list, see [here](https://bolajiwahab.github.io/pgrubic/rules/).

## Formatting style

Pgrubic uses **River** style code formatting.

## Contributing

We welcome and greatly appreciate contributions. If you would like to contribute, please see the [contributing guidelines](https://github.com/bolajiwahab/pgrubic/blob/main/CONTRIBUTING.md).

## Support

Encountering issues? Take a look at the existing GitHub [issues](https://github.com/bolajiwahab/pgrubic/issues), and don't hesitate to open a new one.

## Acknowledgments

Pgrubic is inspired by a number of similar tools such as [Strong Migrations](https://github.com/ankane/strong_migrations), [squabble](https://github.com/erik/squabble),
[squawk](https://github.com/sbdchd/squawk), [pgextwlist](https://github.com/dimitri/pgextwlist), [Don't_Do_This](https://wiki.postgresql.org/wiki/Don't_Do_This)
and [schemalint](https://github.com/kristiandupont/schemalint).

Pgrubic is built upon the shoulders of:

- [pglast](https://github.com/lelit/pglast) - Python bindings to libpg_query
- [libpg_query](https://github.com/pganalyze/libpg_query) - PostgreSQL parser outside of the server environment

## License

Pgrubic is released under GPL-3.0 license.
