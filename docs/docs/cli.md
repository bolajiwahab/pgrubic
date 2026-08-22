# Command line interface

## pgrubic

```text
Pgrubic: A PostgreSQL linter and formatter for schema migrations and design best
practices.

Usage: pgrubic [OPTIONS] COMMAND [ARGS]...

Commands:
  format  Run the SQL formatter on the given files or directories.
  lint    Run the SQL linter on the given files or directories.

Options:
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Configuration overrides:
  Pass a TOML `<KEY> = <VALUE>` pair. May be repeated.
    --config "lint.target-postgres-version = 17"
    --config 'format.type-casting-style = "native"'

Examples:
  pgrubic lint .
  pgrubic lint --fix migrations/
  pgrubic format schema.sql
  pgrubic format --check migrations/
```

## lint

```text
Run the SQL linter on the given files or directories.

Usage: pgrubic lint [OPTIONS] [SOURCES]...

Options:
  --fix                          Apply fixes to resolve lint violations.
  --ignore-noqa                  Ignore inline `-- noqa` directives.
  --add-file-level-general-noqa  Add `-- pgrubic: noqa` to the beginning of each
                                 SQL file, causing the entire file to be ignored
                                 by the linter.
  --generate-lint-report         Generate a lint report.
  -e, --exit-zero                Exit with status code "0", even when lint
                                 violations are present.
  --config <CONFIG_OPTION>       A TOML `<KEY> = <VALUE>` pair overriding a
                                 configuration option. May be repeated. Command-
                                 line overrides always take precedence over
                                 configuration files.

                                 Examples:
                                   --config "lint.target-postgres-version = 17"
                                   --config 'format.type-casting-style = "native"'
  --verbose                      Enable verbose logging.
  --workers INTEGER              Number of workers to use. Defaults to the
                                 number of CPUs or the value of PGRUBIC_WORKERS.
  -v, --version                  Show the version and exit.
  -h, --help                     Show this message and exit.
```

## format

```text
Run the SQL formatter on the given files or directories.

Usage: pgrubic format [OPTIONS] [SOURCES]...

Options:
  --check                   Check if any files would be reformatted.
  --diff                    Report the difference between the current file and
                            what the formatted file would look like.
  --no-cache                Disable cache reads.
  --config <CONFIG_OPTION>  A TOML `<KEY> = <VALUE>` pair overriding a
                            configuration option. May be repeated. Command-line
                            overrides always take precedence over configuration
                            files.

                            Examples:
                              --config "lint.target-postgres-version = 17"
                              --config 'format.type-casting-style = "native"'
  --verbose                 Enable verbose logging.
  --workers INTEGER         Number of workers to use. Defaults to the number of
                            CPUs or the value of PGRUBIC_WORKERS.
  -v, --version             Show the version and exit.
  -h, --help                Show this message and exit.
```

## Exit codes

When using **pgrubic** as a command line tool, it returns [exit-code](https://shapeshed.com/unix-exit-codes/) which can be useful in CI pipelines.

### lint

| Code | Description                                                    |
| ---- | -------------------------------------------------------------- |
| 0    | No violations found or all violations were fixed automatically |
| 1    | Violations found                                               |
| 2    | Error occurred during linting                                  |

### format

| Code |                    Description                          |
| ---- | --------------------------------------------------------|
| 0    | Formatting was successful, even if no changes were made |
| 2    | Error occurred during formatting                        |

#### --check

| Code |           Description            |
| -----| ---------------------------------|
| 0    | No changes would be made         |
| 1    | Changes would be made            |
| 2    | Error occurred during formatting |

#### --diff

| Code |           Description            |
| ---- | ---------------------------------|
| 0    | No changes would be made         |
| 1    | Changes would be made            |
| 2    | Error occurred during formatting |
