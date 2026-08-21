# Configuring pgrubic

**pgrubic** is configured via the `pgrubic.toml` configuration file in either the current directory, up to the root directory or the path set by the `PGRUBIC_CONFIG_PATH` environment variable.

## Discovery

**pgrubic** recursively searches for the configuration file by starting in the current directory and moving up one level at a time until it either finds the file or reaches the root directory.

When `PGRUBIC_CONFIG_PATH` environment variable is set, **pgrubic** will first search for the configuration file at the path set by `PGRUBIC_CONFIG_PATH` and if it does not find the file, it will search for the configuration file in the same way as described above.

If after searching for the configuration file, the configuration file is not found, **pgrubic** will then fall back to the default configuration.

## Sections

There are three sections in the configuration file: `global`, `lint` and `format`.

The `global` section is used to configure global settings for **pgrubic**. Its section is the top level section in the configuration file hence it is not named.

The `lint` section is used to configure lint-specific settings for **pgrubic**.

The `format` section is used to configure format-specific settings for **pgrubic**.

## Default Configuration

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

To learn more about each setting, see [**settings**](settings.md).
