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
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Socket Badge](https://socket.dev/api/badge/pypi/package/pgrubic?artifact_id=tar-gz)](https://socket.dev/pypi/package/pgrubic/overview/)
[![Dependency Review](https://img.shields.io/badge/Dependency%20Review-enabled-deepgreen)](https://github.com/bolajiwahab/pgrubic/actions/workflows/dependency-review.yml)

pgrubic is a PostgreSQL linter and formatter for schema migrations and design best practices.

## Features

- Over 100+ rules
- Automatic violation correction (e.g., automatically add `concurrently` to index create statements)
- River style code formatting for DML statements
- Almost identical styling with **pg_dump** for DDL statements
- Python 3.12+ compatibility
- Automatic caching to avoid reformatting unchanged files
- Violations suppression, statement level, and file level
- Can be used as a library in your own Python projects, not just as a CLI tool

## Getting Started

For more, see the [documentation](https://bolajiwahab.github.io/pgrubic/).

## Installation

**<span style="color:red">pgrubic is only supported on Python 3.12 or higher</span>**.

### via PyPI

```bash
pip install pgrubic
```

### via GitHub

```bash
pip install git+https://github.com/bolajiwahab/pgrubic.git
```

### via Docker

```bash
docker run --rm -it -v $PWD:/sql ghcr.io/bolajiwahab/pgrubic:2.0.0 lint *.sql     # Lint SQL files
docker run --rm -it -v $PWD:/sql ghcr.io/bolajiwahab/pgrubic:2.0.0 format *.sql   # Format SQL files
```

### via Github Action

```yaml
- uses: azellarhq/pgrubic-action@v2
  with:
    src: "./src"
    pgrubic-version: "2.0.0"
```

### via Playground

Lint, format, and fix your migrations directly in your browser, no installation required: [pgrubic Playground](https://pgrubic.azellar.com/)

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

pgrubic can also be used as a pre-commit hook:

```
- repo: https://github.com/bolajiwahab/pgrubic
  rev: 2.0.0
  hooks:
    - id: pgrubic-lint
    - id: pgrubic-format
```

## Configuration

pgrubic can be configured via the [`pgrubic.toml`] file in either the current directory, up to the root directory or the path set by the `PGRUBIC_CONFIG_PATH` environment variable.

The following configuration options are available in the [`pgrubic.toml`] with the following defaults:

<!-- BEGIN GENERATED DEFAULT CONFIG -->

```toml
cache-dir = ".pgrubic_cache"
include = []
exclude = []
respect-gitignore = true
[lint]
target-postgres-version = 14
additional-non-volatile-functions = []
select = []
ignore = []
include = []
exclude = []
ignore-noqa = false
disallowed-schemas = []
allowed-extensions = []
allowed-languages = []
fix = false
fixable = []
unfixable = []
disallowed-data-types = []
required-columns = []
timestamp-column-suffix = "_at"
date-column-suffix = "_date"
regex-partition = "^.+$"
regex-index = "^.+$"
regex-constraint-primary-key = "^.+$"
regex-constraint-unique-key = "^.+$"
regex-constraint-foreign-key = "^.+$"
regex-constraint-check = "^.+$"
regex-constraint-exclusion = "^.+$"
regex-sequence = "^.+$"

[format]
include = []
exclude = []
comma-at-beginning = true
compact-parenthesized-lists-margin = 90
uppercase-keywords = true
type-casting-style = "standard"
rewrite-function-calls-as-equivalent-syntax = true
new-line-before-semicolon = false
remove-pg-catalog-from-functions = true
remove-default-index-access-method = true
lines-between-statements = 1
check = false
diff = false
no-cache = false
```

<!-- END GENERATED DEFAULT CONFIG -->

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

pgrubic uses **River** style code formatting.

## Contributing

We welcome and greatly appreciate contributions. If you would like to contribute, please see the [contributing guidelines](https://github.com/bolajiwahab/pgrubic/blob/main/docs/docs/contributing.md).

## Support

Encountering issues? Take a look at the existing GitHub [issues](https://github.com/bolajiwahab/pgrubic/issues), and don't hesitate to open a new one.

## Acknowledgments

pgrubic is inspired by a number of similar tools such as [Strong Migrations](https://github.com/ankane/strong_migrations), [squabble](https://github.com/erik/squabble),
[squawk](https://github.com/sbdchd/squawk), [pgextwlist](https://github.com/dimitri/pgextwlist), [Don't_Do_This](https://wiki.postgresql.org/wiki/Don't_Do_This)
and [schemalint](https://github.com/kristiandupont/schemalint).

pgrubic is built upon the shoulders of:

- [pglast](https://github.com/lelit/pglast) - Python bindings to libpg_query
- [libpg_query](https://github.com/pganalyze/libpg_query) - PostgreSQL parser outside of the server environment

## License

pgrubic is released under GPL-3.0 license.
