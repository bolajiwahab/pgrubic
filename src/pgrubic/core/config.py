"""Configuration."""

import os
import typing
import pathlib
import dataclasses

import toml
from deepmerge import always_merger

from pgrubic import PACKAGE_NAME
from pgrubic.core import errors
from pgrubic.core.logger import logger

CONFIG_FILE: typing.Final[str] = f"{PACKAGE_NAME}.toml"

DEFAULT_CONFIG: typing.Final[pathlib.Path] = (
    pathlib.Path(__file__).resolve().parent.parent / CONFIG_FILE
)

CONFIG_PATH_ENVIRONMENT_VARIABLE: typing.Final[str] = (
    f"{PACKAGE_NAME.upper()}_CONFIG_PATH"
)


@dataclasses.dataclass(kw_only=True, frozen=True)
class DisallowedSchema:
    """Representation of disallowed schema."""

    name: str
    reason: str
    use_instead: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class DisallowedDataType:
    """Representation of disallowed data type."""

    name: str
    reason: str
    use_instead: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class Column:
    """Representation of column."""

    name: str
    data_type: str


@dataclasses.dataclass(kw_only=True)
class Lint:
    # fmt: off
    """
### **postgres-target-version**
The target version of Postgres to lint against. This is used to either enable or
disable certain linting rules. For example, `DETACH PARTITION CONCURRENTLY`
was introduced from Postgres 14.

**Type**: `int`

**Default**: `14`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
postgres-target-version = 12
```
</details>

### **select**
List of rule aliases or prefixes to enable. It can be the exact code of a rule or
an entire category of rules, for example, `TP017`, `TP`. All rules are enabled by default.
Can be used in combination with `ignore` to streamline rules selection.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
select = ["TP"]
```
</details>

### **ignore**
List of rule aliases or prefixes to disable. It can be the exact code of a rule or
an entire category of rules, for example, `TP017`, `TP`.
Can be used in combination with `select` to streamline rules selection.
Please note that **ignore** takes precedence over **select**.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
ignore = ["TP017"]
```
</details>

### **include**
List of file patterns to include in the linting process.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
include = ["V*.sql"]
```
</details>

### **exclude**
List of file patterns to exclude from the linting process.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
exclude = ["test*.sql"]
```
</details>

### **ignore-noqa**
Whether to ignore `NOQA` directives in sources.
Overridden by the `--ignore-noqa` command-line flag.

**Type**: `bool`

**Default**: `False`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
ignore-noqa = true
```
</details>

### **allowed-extensions**
List of allowed postgres extensions.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
allowed-extensions = ["pg_stat_statements"]
```
</details>

### **allowed-languages**
List of allowed languages.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
allowed-languages = ["plpgsql"]
```
</details>

### **required-columns**
List of required columns along with their data types for every table.

**Type**: `list[Column]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
required-columns = [
    { name = "created_at", data_type = "timestamptz" },
    { name = "updated_at", data_type = "timestamptz" },
]
```
</details>

### **disallowed-schemas**
List of disallowed schemas, with reasons for their disallowance and what to use
instead.

**Type**: `list[DisallowedSchema]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
disallowed-schemas = [
    { name = "public", reason = "public schema", use_instead = "app" },
]
```
</details>

### **disallowed-data-types**
List of disallowed data types, with reasons for their disallowance
and what to use instead.

**Type**: `list[DisallowedDataType]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
disallowed-data-types = [
    { name = "varchar", reason = "text is better", use_instead = "text" },
]
```
</details>

### **fix**
Whether to automatically fix fixable violations.
Overridden by the `--fix` command-line flag.

**Type**: `bool`

**Default**: `False`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
fix = true
```
</details>

### **fixable**
List of rule aliases or prefixes to consider fixable. It can be the exact code of a rule
or an entire category of rules, for example, `TP017`, `TP`. All rules are considered
fixable by default. Please note that **unfixable** takes precedence over **fixable**.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
fixable = ["TP"]
```
</details>

### **unfixable**
List of rule aliases or prefixes to consider unfixable. It can be the exact code of a rule
or an entire category of rules, for example, `TP017`, `TP`.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
unfixable = ["TP017"]
```
</details>

### **timestamp-column-suffix**
Suffix to add to timestamp columns.

**Type**: `str`

**Default**: `"_at"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
timestamp-column-suffix = "_at"
```
</details>

### **date-column-suffix**
Suffix to add to date columns.

**Type**: `str`

**Default**: `"_on"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
date-column-suffix = "_date"
```
</details>

### **regex-partition**
Regular expression to match partition names.

**Type**: `str`

**Default**: `r"^[a-z0-9_]+$"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
regex-partition = r"^[a-z0-9_]+$"
```
</details>

### **regex-index**
Regular expression to match index names.

**Type**: `str`

**Default**: `r"^[a-z0-9_]+$"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
regex-index = r"^[a-z0-9_]+$"
```
</details>

### **regex-constraint-primary-key**
Regular expression to match primary key constraint names.

**Type**: `str`

**Default**: `r"^[a-z0-9_]+$"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
regex-constraint-primary-key = r"^[a-z0-9_]+$"
```
</details>

### **regex-constraint-unique-key**
Regular expression to match unique key constraint names.

**Type**: `str`

**Default**: `r"^[a-z0-9_]+$"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
regex-constraint-unique-key = r"^[a-z0-9_]+$"
```
</details>

### **regex-constraint-foreign-key**
Regular expression to match foreign key constraint names.

**Type**: `str`

**Default**: `r"^[a-z0-9_]+$"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
regex-constraint-foreign-key = r"^[a-z0-9_]+$"
```
</details>

### **regex-constraint-check**
Regular expression to match check constraint names.

**Type**: `str`

**Default**: `r"^[a-z0-9_]+$"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
regex-constraint-check = r"^[a-z0-9_]+$"
```
</details>

### **regex-constraint-exclusion**
Regular expression to match exclusion constraint names.

**Type**: `str`

**Default**: `r"^[a-z0-9_]+$"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
regex-constraint-exclusion = r"^[a-z0-9_]+$"
```
</details>

### **regex-sequence**
Regular expression to match sequence names.

**Type**: `str`

**Default**: `r"^[a-z0-9_]+$"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
regex-sequence = r"^[a-z0-9_]+$"
```
</details>
    """  # noqa: D212, D207 # fmt: on

    postgres_target_version: int
    select: list[str]
    ignore: list[str]
    include: list[str]
    exclude: list[str]
    ignore_noqa: bool
    allowed_extensions: list[str]
    allowed_languages: list[str]
    required_columns: list[Column]
    disallowed_schemas: list[DisallowedSchema]
    disallowed_data_types: list[DisallowedDataType]

    fix: bool
    fixable: list[str]
    unfixable: list[str]

    timestamp_column_suffix: str
    date_column_suffix: str
    regex_partition: str
    regex_index: str
    regex_constraint_primary_key: str
    regex_constraint_unique_key: str
    regex_constraint_foreign_key: str
    regex_constraint_check: str
    regex_constraint_exclusion: str
    regex_sequence: str


@dataclasses.dataclass(kw_only=True)
class Format:
    # fmt: off
    """
### **include**
A list of file patterns to include in the formatting process.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
include = ["V*.sql"]
```
</details>

### **exclude**
A list of file patterns to exclude from the formatting process.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
exclude = ["test*.sql"]
```
</details>

### **comma-at-beginning**
If `true`, add comma as a prefix as opposed to a suffix when formatting a list of
items, such as list of columns in which each column is on a separate line.

For example, when `true`:
```sql
select column1
     , column2
     , column3
     , .......
```

when `false`:
```sql
select column1,
       column2,
       column3,
       .......
```

**Type**: `bool`

**Default**: `true`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
comma-at-beginning = false
```
</details>

### **new-line-before-semicolon**
If `true`, add a new line before each semicolon.

For example, when `true`:
```sql
select column1
        , column2
        , column3
    from table
;
```

when `false`:
```sql
select column1,
        column2,
        column3
    from table;
```

**Type**: `bool`

**Default**: `false`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
new-line-before-semicolon = true
```
</details>

### **lines-between-statements**
Number of lines between SQL statements.

**Type**: `int`

**Default**: `1`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
lines-between-statements = 2
```
</details>

### **remove-pg-catalog-from-functions**
If `true`, remove the `pg_catalog.` prefix from functions. Postgres standard functions
are located in the `pg_catalog` schema and thus prefixed with `pg_catalog.`
by default.

**Type**: `bool`

**Default**: `true`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
remove-pg-catalog-from-functions = false
```
</details>

### **diff**
When `true`, report the difference between the current file and how it will look when
formatted, without making any changes to the file. If there is a difference, it exits
with a non-zero exit code.

Overridden by the `--diff` command-line flag.

**Type**: `bool`

**Default**: `false`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
diff = true
```
</details>

### **check**
When `true`, it exits with a non-zero exit code if the any files would have been
modified by the formatter.

Overridden by the `--check` command-line flag.

**Type**: `bool`

**Default**: `false`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
check = true
```
</details>

### **no-cache**
Whether to read the cache. Caching helps speed up the formatting process. When a file
has not been modified after the last formatting, it is simply skipped.
To force reformatting of a file even if it has not been modified since the last
formatting, set to `true`.

Overridden by the `--no-cache` command-line flag.

**Type**: `bool`

**Default**: `false`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
no-cache = true
```
</details>
    """  # noqa: D212, D207 # fmt: on

    include: list[str]
    exclude: list[str]
    comma_at_beginning: bool
    new_line_before_semicolon: bool
    lines_between_statements: int
    remove_pg_catalog_from_functions: bool
    diff: bool
    check: bool
    no_cache: bool


@dataclasses.dataclass(kw_only=True)
class Config:
    # fmt: off
    """
### **cache-dir**
Path to the cache directory.

If default and the environment variable `PGRUBIC_CACHE` is set, the environment
variable takes precedence or otherwise the non-default set value is always used.

**Type**: `str`

**Default**: `".pgrubic_cache"`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
cache-dir = "~/.cache/pgrubic"
```
</details>

### **include**
A list of file patterns to include in the linting and formatting process.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
include = ["V*.sql"]
```
</details>

### **exclude**
A list of file patterns to exclude from the linting and formatting process.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
exclude = ["test*.sql"]
```
</details>

### **respect-gitignore**
Whether to automatically exclude files that are ignored by `.ignore`, `.gitignore`,
`.git/info/exclude`, and global gitignore files. Enabled by default.

**Type**: `bool`

**Default**: `True`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
respect_gitignore = false
```
</details>
    """  # noqa: D212, D207 # fmt: on

    cache_dir: pathlib.Path

    include: list[str]
    exclude: list[str]
    respect_gitignore: bool

    lint: Lint
    format: Format


def _load_default_config() -> dict[str, typing.Any]:
    """Load default config."""
    return dict(toml.load(DEFAULT_CONFIG))


def _load_user_config() -> dict[str, typing.Any]:
    """Load config from absolute path config file."""
    config_file_absolute_path = _get_config_file_absolute_path()

    if config_file_absolute_path:
        return dict(toml.load(config_file_absolute_path))

    return {}  # pragma: no cover


def _merge_config() -> dict[str, typing.Any]:
    """Merge default and user config."""
    return dict(always_merger.merge(_load_default_config(), _load_user_config()))


def _get_config_file_absolute_path(
    config_file: str = CONFIG_FILE,
) -> pathlib.Path | None:
    """Get the absolute path of the config file.
    If CONFIG_PATH_ENVIRONMENT_VARIABLE environment variable is set, we try to use that
    else, we use the first config file that we find upwards from the current working
    directory.
    """
    env_config_path = os.getenv(CONFIG_PATH_ENVIRONMENT_VARIABLE)

    if env_config_path:
        config_file_absolute_path = pathlib.Path(env_config_path).resolve() / config_file
        if pathlib.Path.exists(config_file_absolute_path):
            logger.info(
                """Using settings from "%s\"""",
                config_file_absolute_path,
            )
            return config_file_absolute_path

    current_directory = pathlib.Path.cwd()

    # Traverse upwards through the directory tree
    while current_directory != current_directory.parent:
        # Check if the configuration file exists
        config_file_absolute_path = current_directory / config_file

        if pathlib.Path.exists(config_file_absolute_path):
            logger.info(
                """Using settings from "%s\"""",
                config_file_absolute_path,
            )
            return config_file_absolute_path

        # Move up one directory
        current_directory = current_directory.parent  # pragma: no cover

    logger.info(
        """Using default settings""",
    )

    return None  # pragma: no cover


def parse_config() -> Config:
    """Parse config."""
    merged_config = _merge_config()
    config_lint = merged_config["lint"]
    config_format = merged_config["format"]

    try:
        return Config(
            cache_dir=pathlib.Path(merged_config["cache-dir"]),
            include=merged_config["include"],
            exclude=merged_config["exclude"],
            respect_gitignore=merged_config["respect-gitignore"],
            lint=Lint(
                postgres_target_version=config_lint["target-postgres-version"],
                select=config_lint["select"],
                ignore=config_lint["ignore"],
                include=config_lint["include"] + merged_config["include"],
                exclude=config_lint["exclude"] + merged_config["exclude"],
                ignore_noqa=config_lint["ignore-noqa"],
                allowed_extensions=config_lint["allowed-extensions"],
                allowed_languages=config_lint["allowed-languages"],
                fix=config_lint["fix"],
                fixable=config_lint["fixable"],
                unfixable=config_lint["unfixable"],
                timestamp_column_suffix=config_lint["timestamp-column-suffix"],
                date_column_suffix=config_lint["date-column-suffix"],
                regex_partition=config_lint["regex-partition"],
                regex_index=config_lint["regex-index"],
                regex_constraint_primary_key=config_lint["regex-constraint-primary-key"],
                regex_constraint_unique_key=config_lint["regex-constraint-unique-key"],
                regex_constraint_foreign_key=config_lint["regex-constraint-foreign-key"],
                regex_constraint_check=config_lint["regex-constraint-check"],
                regex_constraint_exclusion=config_lint["regex-constraint-exclusion"],
                regex_sequence=config_lint["regex-sequence"],
                required_columns=[
                    Column(
                        name=column["name"],
                        data_type=column["data-type"],
                    )
                    for column in config_lint["required-columns"]
                ],
                disallowed_data_types=[
                    DisallowedDataType(
                        name=data_type["name"],
                        reason=data_type["reason"],
                        use_instead=data_type["use-instead"],
                    )
                    for data_type in config_lint["disallowed-data-types"]
                ],
                disallowed_schemas=[
                    DisallowedSchema(
                        name=schema["name"],
                        reason=schema["reason"],
                        use_instead=schema["use-instead"],
                    )
                    for schema in config_lint["disallowed-schemas"]
                ],
            ),
            format=Format(
                include=config_format["include"] + merged_config["include"],
                exclude=config_format["exclude"] + merged_config["exclude"],
                comma_at_beginning=config_format["comma-at-beginning"],
                new_line_before_semicolon=config_format["new-line-before-semicolon"],
                lines_between_statements=config_format["lines-between-statements"],
                remove_pg_catalog_from_functions=config_format[
                    "remove-pg-catalog-from-functions"
                ],
                diff=config_format["diff"],
                check=config_format["check"],
                no_cache=config_format["no-cache"],
            ),
        )
    except KeyError as error:
        msg = "Missing config key: "
        raise errors.MissingConfigError(msg + error.args[0]) from error
