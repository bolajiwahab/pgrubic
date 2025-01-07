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

# Report if files would have been modified, returning a non-zero exit code as well
# the difference between the current file and how the formatted file would look like
diff = false

# Whether to read the cache.
no-cache = false
```

To learn more about each setting, see [**settings**](settings.md).
