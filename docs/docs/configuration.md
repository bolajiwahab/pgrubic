# Configuring pgrubic

**pgrubic** is configured via the `pgrubic.toml` configuration file in either the current directory, up to the root directory or the path set by the `PGRUBIC_CONFIG_PATH` environment variable.

## Discovery

**pgrubic** recursively searches for the configuration file by starting in the current directory and moving up one level at a time until it either finds the file or reaches the root directory.

When `PGRUBIC_CONFIG_PATH` environment variable is set, **pgrubic** will first search for the configuration file at the path set by `PGRUBIC_CONFIG_PATH` and if it does not find the file, it will search for the configuration file in the same way as described above.

If after searching for the configuration file, the configuration file is not found, **pgrubic** will then fall back to the default configuration.

Config values can also be overridden using the `--config <CONFIG_OPTION>` command-line argument.

## Sections

There are three sections in the configuration file: `global`, `lint` and `format`.

The `global` section is used to configure global settings for **pgrubic**. Its section is the top level section in the configuration file hence it is not named.

The `lint` section is used to configure lint-specific settings for **pgrubic**.

The `format` section is used to configure format-specific settings for **pgrubic**.

## Default Configuration

<!-- BEGIN GENERATED DEFAULT CONFIG -->

```toml
# Path to the cache directory
cache-dir = ".pgrubic_cache"

# Include all files
include = []

# Exclude no files
exclude = []

# Respect gitignore
respect-gitignore = true

[lint]
# Target version 14 of PostgreSQL
target-postgres-version = 14

# Enable all rules
select = []

# Disable no rules
ignore = []

# Include all files
include = []

# Exclude no files
exclude = []

# Ignore suppressing violations that are marked as `noqa`
ignore-noqa = false

# List of additional non-volatile functions
additional-non-volatile-functions = []

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

# Suffix Timestamp columns with `_at`
timestamp-column-suffix = "_at"

# Suffix Date columns with suffix `_date`
date-column-suffix = "_date"

# Allow any naming convention for partitions
regex-partition = "^.+$"

# Allow any naming convention for indexes
regex-index = "^.+$"

# Allow any naming convention for primary key constraints
regex-constraint-primary-key = "^.+$"

# Allow any naming convention for unique keys
regex-constraint-unique-key = "^.+$"

# Allow any naming convention for foreign keys
regex-constraint-foreign-key = "^.+$"

# Allow any naming convention for check constraints
regex-constraint-check = "^.+$"

# Allow any naming convention for exclusion constraints
regex-constraint-exclusion = "^.+$"

# Allow any naming convention for sequences
regex-sequence = "^.+$"

[format]
# Include all files
include = []

# Exclude no files
exclude = []

# Comma at the beginning of an item
comma-at-beginning = true

# Compact parenthesized lists margin of 90
compact-parenthesized-lists-margin = 90

# Uppercase keywords
uppercase-keywords = true

# Type casting style is standard
# CAST(value AS type)
type-casting-style = "standard"

# Rewrite some function calls using their equivalent SQL syntax.
# For example, pg_catalog.timezone('UTC', value) is formatted as "value AT TIME ZONE 'UTC'"
rewrite-function-calls-as-equivalent-syntax = true

# Do not place the semicolon on a new line
new-line-before-semicolon = false

# Remove pg_catalog from functions
remove-pg-catalog-from-functions = true

# Remove default index access method (btree)
remove-default-index-access-method = true

# Separate statements by N new lines (default: 1)
lines-between-statements = 1

# Check if files would have been modified, returning a non-zero exit code
check = false

# Report if files would have been modified, returning a non-zero exit code as well as the difference between the current file and how the formatted file would look like
diff = false

# Whether to read the cache.
no-cache = false
```

<!-- END GENERATED DEFAULT CONFIG -->

To learn more about each setting, see [**settings**](settings.md).
