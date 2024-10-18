## Pgrubic

Pgrubic is a PostgreSQL linter and formatter for schema migrations and design best practices.

## Features
- Over 100+ rules.
- Automatic violation correction (e.g., automatically add `concurrently` to index create statements).
- River style code formatting.

## Getting Started
For more, see the [documentation](https://bolajiwahab.github.io/pgrubic/).

## Installation
```bash
pip install pgrubic
```
**<span style="color:red">Pgrubic is only supported on Python 3.12+</span>**.

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
pgrubic lint file.sql --fix          # Lint `file.sql` and fix violations automatically
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
  # Ruff version.
  rev: v1.0.0
  hooks:
    # Run the linter.
    - id: pgrubic-lint
      name: Lint PSQL files
      args: [lint, --fix]
      types: [sql]
    # Run the formatter.
    - id: pgrubic-format
      name: Format PSQL files
      args: [format, --check, --diff]
      types: [sql]
```
## Configuration
Pgrubic can be configured via the [`pgrubic.toml`] file in either the current directory or in the user's home directory.

## Rules

## Contributing

## Support

## Acknowledgments

## License
