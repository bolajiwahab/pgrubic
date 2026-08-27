"""Configuration."""

import os
import enum
import typing
import difflib
import pathlib

import toml
from pydantic import (
    Field,
    BaseModel,
    ConfigDict,
    BeforeValidator,
    ValidationError,
    create_model,
)
from deepmerge import merger
from pydantic.fields import FieldInfo

from pgrubic import PACKAGE_NAME
from pgrubic.core import enums, errors
from pgrubic.core.logger import logger

CONFIG_FILE: typing.Final[str] = f"{PACKAGE_NAME}.toml"

_DEFAULT_CONFIG_PATH: typing.Final[pathlib.Path] = (
    pathlib.Path(__file__).resolve().parent.parent / CONFIG_FILE
)

# Maintain for backward compatibility. To be deprecated
DEFAULT_CONFIG: typing.Final[pathlib.Path] = _DEFAULT_CONFIG_PATH

CONFIG_PATH_ENVIRONMENT_VARIABLE: typing.Final[str] = (
    f"{PACKAGE_NAME.upper()}_CONFIG_PATH"
)

_CONFIG_MERGER: typing.Final[merger.Merger] = merger.Merger(
    type_strategies=[(dict, ["merge"]), (list, ["override"])],
    fallback_strategies=["override"],
    type_conflict_strategies=["override"],
)


class ConfigScope(enum.StrEnum):
    """Configuration scope."""

    GENERAL = enum.auto()
    FILESYSTEM = enum.auto()
    INVOCATION = enum.auto()


_ConfigValue = typing.TypeVar("_ConfigValue")
GeneralConfigValue = typing.Annotated[_ConfigValue, ConfigScope.GENERAL]
FilesystemConfigValue = typing.Annotated[_ConfigValue, ConfigScope.FILESYSTEM]
InvocationConfigValue = typing.Annotated[_ConfigValue, ConfigScope.INVOCATION]


def _parse_type_casting_style(value: object) -> enums.TypeCastingStyle:
    """Parse the configured type-casting style."""
    valid_values = tuple(style.value for style in enums.TypeCastingStyle)

    if isinstance(value, str):
        try:
            return enums.TypeCastingStyle(value)
        except ValueError:
            suggestion = difflib.get_close_matches(value, valid_values, n=1)
    else:
        suggestion = []

    msg = ""
    if suggestion:
        msg += f'Did you mean "{suggestion[0]}"? '

    valid_values_str = ", ".join(f'"{v}"' for v in valid_values)
    msg += f"Expected one of: {valid_values_str}"

    raise ValueError(msg)


def _parse_additional_non_volatile_functions(value: object) -> object:
    """Parse configured additional non-volatile functions."""
    if isinstance(value, list):
        return frozenset(value)
    return value


def _parse_cache_dir(value: object) -> object:
    """Parse configured cache directory."""
    if isinstance(value, str):
        return pathlib.Path(value)
    return value


class BaseConfig(BaseModel):
    """Base configuration model."""

    model_config = ConfigDict(
        alias_generator=lambda field_name: field_name.replace("_", "-"),
        extra="forbid",
        populate_by_name=True,
        strict=True,
    )


class DisallowedSchema(BaseConfig):
    """Representation of disallowed schema."""

    name: str
    reason: str
    use_instead: str


class DisallowedDataType(BaseConfig):
    """Representation of disallowed data type."""

    name: str
    reason: str
    use_instead: str


class Column(BaseConfig):
    """Representation of column."""

    name: str
    data_type: str


class Lint(BaseConfig):
    # fmt: off
    """
### **target-postgres-version**
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
target-postgres-version = 14
```
</details>

### **additional-non-volatile-functions**
List of additional non-volatile functions. This is used to add to the list of known
non-volatile functions, to check if a default value is volatile or not.
For example, `pg_catalog.clock_timestamp()` is a volatile function, but if you have a
custom function that is non-volatile, you can add it to this list in form
of `schema.function_name`.

Should be used judiciously.

**Type**: `list[str]`

**Default**: `[]`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
additional-non-volatile-functions = ["my_schema.my_non_volatile_function"]
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
    { name = "created_at", data-type = "timestamptz" },
    { name = "updated_at", data-type = "timestamptz" },
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

    target_postgres_version: GeneralConfigValue[int]
    additional_non_volatile_functions: typing.Annotated[
        GeneralConfigValue[frozenset[str]],
        BeforeValidator(_parse_additional_non_volatile_functions),
    ]
    select: GeneralConfigValue[list[str]]
    ignore: GeneralConfigValue[list[str]]
    include: FilesystemConfigValue[list[str]]
    exclude: FilesystemConfigValue[list[str]]
    ignore_noqa: GeneralConfigValue[bool]
    allowed_extensions: GeneralConfigValue[list[str]]
    allowed_languages: GeneralConfigValue[list[str]]
    required_columns: GeneralConfigValue[list[Column]]
    disallowed_schemas: GeneralConfigValue[list[DisallowedSchema]]
    disallowed_data_types: GeneralConfigValue[list[DisallowedDataType]]

    # `fix` makes the linter return fixed source code; it does not write files itself.
    # It is invocation-scoped because each caller controls the result: the CLI writes
    # it to disk, while a UI can expose it through a request option.
    fix: InvocationConfigValue[bool]
    fixable: GeneralConfigValue[list[str]]
    unfixable: GeneralConfigValue[list[str]]

    timestamp_column_suffix: GeneralConfigValue[str]
    date_column_suffix: GeneralConfigValue[str]
    regex_partition: GeneralConfigValue[str]
    regex_index: GeneralConfigValue[str]
    regex_constraint_primary_key: GeneralConfigValue[str]
    regex_constraint_unique_key: GeneralConfigValue[str]
    regex_constraint_foreign_key: GeneralConfigValue[str]
    regex_constraint_check: GeneralConfigValue[str]
    regex_constraint_exclusion: GeneralConfigValue[str]
    regex_sequence: GeneralConfigValue[str]


class Format(BaseConfig):
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

### **compact-parenthesized-lists-margin**
Use a compact, single-line form for a parenthesized list when it does not exceed this
margin. Set it to `0` to always expand parenthesized lists.

**Type**: `int`

**Default**: `90`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
compact-parenthesized-lists-margin = 100
```
</details>

### **uppercase-keywords**
Whether to format SQL keywords in uppercase. When `false`, keywords are formatted in
lowercase.

**Type**: `bool`

**Default**: `true`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
uppercase-keywords = false
```
</details>

### **type-casting-style**
The type-casting style to use. Can be one of `native`, `standard` or `literal`.

Native style uses `value::type_name`, standard style uses `CAST(value AS type_name)`
and literal style uses `type_name value`.

!!! note
    Literal style is applied only when the typed-literal syntax is semantically
    equivalent. When a cast cannot be converted safely, such as an implicit-length
    `char` cast or a cast of a non-string expression, its original standard or
    native syntax is preserved.

    For example, these casts can safely use literal syntax:

    ```sql
    CAST('xyz' AS text)    -> text 'xyz'
    'xyz'::char(3)         -> char(3) 'xyz'
    ```

    These casts retain their original syntax:

    ```sql
    CAST('xyz' AS char)    -> CAST('xyz' AS char)
    'xyz'::char            -> 'xyz'::char
    1::text                -> 1::text
    CAST(1 + 1 AS text)    -> CAST(1 + 1 AS text)
    ```

**Type**: `str`

**Default**: `standard`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
type-casting-style = "native"
```
</details>

### **rewrite-function-calls-as-equivalent-syntax**
If `true`, rewrite some function calls using their equivalent SQL syntax. For example,
`pg_catalog.timezone('UTC', value)` is formatted as
`value AT TIME ZONE 'UTC'`.

**Type**: `bool`

**Default**: `true`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
rewrite-function-calls-as-equivalent-syntax = false
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

### **remove-default-index-access-method**
If `true`, remove the `USING btree` clause from index definitions. B-tree is the default
index access method in PostgreSQL and thus can be omitted.

**Type**: `bool`

**Default**: `true`

**Example**:
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
remove-default-index-access-method = false
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
Whether to read the cache. Caching speeds up formatting by skipping files whose
content, format settings, and pgrubic version all match a previous run, since
re-running the formatter on them would just reproduce what's already on disk.

Set to `true` to bypass the cache and re-run the formatter on every file this run,
regardless of what the cache says. This does not force a file to be rewritten:
a file is only ever written when the formatter's output actually differs from
what's on disk, cache or no cache.

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

    include: FilesystemConfigValue[list[str]]
    exclude: FilesystemConfigValue[list[str]]
    comma_at_beginning: GeneralConfigValue[bool]
    compact_parenthesized_lists_margin: GeneralConfigValue[int]
    uppercase_keywords: GeneralConfigValue[bool]
    type_casting_style: typing.Annotated[
        GeneralConfigValue[enums.TypeCastingStyle],
        BeforeValidator(_parse_type_casting_style),
    ]
    rewrite_function_calls_as_equivalent_syntax: GeneralConfigValue[bool]
    new_line_before_semicolon: GeneralConfigValue[bool]
    lines_between_statements: GeneralConfigValue[int]
    remove_pg_catalog_from_functions: GeneralConfigValue[bool]
    remove_default_index_access_method: GeneralConfigValue[bool]
    diff: InvocationConfigValue[bool]
    check: InvocationConfigValue[bool]
    no_cache: InvocationConfigValue[bool]


class Config(BaseConfig):
    # fmt: off
    """
### **cache-dir**
Path to the cache directory.

If default and the environment variable `PGRUBIC_CACHE_DIR` is set, the environment
variable takes precedence or otherwise the non-default set value is always used.

**Type**: `str`

**Default**: `".pgrubic_cache"`

**Environment Variable**: `PGRUBIC_CACHE_DIR`

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
respect-gitignore = false
```
</details>
    """  # noqa: D212, D207 # fmt: on

    cache_dir: typing.Annotated[
        FilesystemConfigValue[pathlib.Path],
        BeforeValidator(_parse_cache_dir),
    ]
    include: FilesystemConfigValue[list[str]]
    exclude: FilesystemConfigValue[list[str]]
    respect_gitignore: FilesystemConfigValue[bool]

    lint: Lint
    format: Format


def load_default_config() -> dict[str, object]:
    """Load default config.

    Returns:
    -------
    dict[str, object]
        The default config.
    """
    return dict(toml.load(_DEFAULT_CONFIG_PATH))


def _config_field_matches_scope(
    field: FieldInfo,
    scope: ConfigScope | None,
) -> bool:
    """Return whether a config field belongs in the requested scope."""
    return any(
        isinstance(metadata, ConfigScope) and (scope is None or metadata is scope)
        for metadata in field.metadata
    )


def _create_config_section_model_from_defaults(
    *,
    name: str,
    source: type[BaseConfig],
    defaults: dict[str, object],
    scope: ConfigScope | None,
) -> type[BaseConfig]:
    """Create a config section model using selected fields and supplied defaults."""
    fields: dict[str, typing.Any] = {}

    for field_name, source_field in source.model_fields.items():
        if not _config_field_matches_scope(source_field, scope):
            continue

        field = source_field.asdict()
        field["attributes"]["validate_default"] = True
        source_annotation = field["annotation"]
        field_annotation = typing.Annotated[
            source_annotation,  # type: ignore[valid-type]
            *field["metadata"],
            Field(**field["attributes"]),
        ]
        fields[field_name] = (
            field_annotation,
            defaults[source_field.alias or field_name],
        )

    return create_model(name, __base__=BaseConfig, **fields)


def _create_config_model_from_defaults(
    *,
    scope: ConfigScope | None,
) -> type[BaseConfig]:
    """Create a config model using packaged defaults."""
    defaults = load_default_config()
    lint_defaults = typing.cast(dict[str, object], defaults["lint"])
    format_defaults = typing.cast(dict[str, object], defaults["format"])

    lint_model = _create_config_section_model_from_defaults(
        name="ConfigLint",
        source=Lint,
        defaults=lint_defaults,
        scope=scope,
    )
    format_model = _create_config_section_model_from_defaults(
        name="ConfigFormat",
        source=Format,
        defaults=format_defaults,
        scope=scope,
    )
    config_base = _create_config_section_model_from_defaults(
        name="ConfigBase",
        source=Config,
        defaults=defaults,
        scope=scope,
    )

    return create_model(
        "Config",
        __base__=config_base,
        lint=(lint_model, Field(default_factory=lint_model)),
        format=(format_model, Field(default_factory=format_model)),
    )


def create_config_model_from_defaults() -> type[BaseConfig]:
    """Create a complete config model using packaged defaults."""
    return _create_config_model_from_defaults(scope=None)


def create_scoped_config_model_from_defaults(
    *,
    scope: ConfigScope,
) -> type[BaseConfig]:
    """Create a scoped config model using packaged defaults.

    Parameters:
    ----------
    scope: ConfigScope
        The scope of the config model.

    Returns:
    -------
    type[BaseConfig]
        The scoped config model.
    """
    return _create_config_model_from_defaults(scope=scope)


def load_default_config_by_scope(*, scope: ConfigScope) -> dict[str, object]:
    """Load packaged defaults for the selected config scope.

    Parameters:
    ----------
    scope: ConfigScope
        The scope of the config to load.

    Returns:
    -------
    dict[str, object]
        The default config for the selected scope.
    """
    model = create_scoped_config_model_from_defaults(scope=scope)
    config = model.model_validate({"lint": {}, "format": {}})
    return config.model_dump(by_alias=True, mode="json")


def _load_user_config() -> dict[str, object]:
    """Load config from absolute path config file.

    Returns:
    -------
    dict[str, object]
        The config from the absolute path config file.
    """
    config_file_absolute_path = _get_config_file_absolute_path()

    if config_file_absolute_path:
        try:
            return dict(toml.load(config_file_absolute_path))
        except toml.decoder.TomlDecodeError as error:
            msg = f"""Error parsing configuration file "{config_file_absolute_path}\""""
            raise errors.ConfigParseError(
                msg,
            ) from error

    return {}  # pragma: no cover


def _merge_config(*, overrides: dict[str, object]) -> dict[str, object]:
    """Merge default and user config, with overrides.

    Parameters:
    ----------
    overrides: dict[str, object]
        Overrides applied on top of the user config.

    Returns:
    -------
    dict[str, object]
        The merged config.
    """
    merged_config = _CONFIG_MERGER.merge(
        load_default_config(),
        _load_user_config(),
    )
    return dict(_CONFIG_MERGER.merge(merged_config, overrides))


def _get_config_file_absolute_path() -> pathlib.Path | None:
    """Get the absolute path of the config file.
    If CONFIG_PATH_ENVIRONMENT_VARIABLE environment variable is set, we try to use that
    else, we use the first config file that we find upwards from the current working
    directory.

    Returns:
    -------
    pathlib.Path | None
        The absolute path of the config file if found, else None.
    """
    env_config_path = os.getenv(CONFIG_PATH_ENVIRONMENT_VARIABLE)

    if env_config_path:
        config_file_absolute_path = pathlib.Path(env_config_path).resolve() / CONFIG_FILE
        if pathlib.Path.exists(config_file_absolute_path):
            logger.info(
                """Using settings from "%s\"""",
                config_file_absolute_path,
            )
            return config_file_absolute_path

        msg = f"""Config file "{CONFIG_FILE}" not found in the path set in the environment variable {CONFIG_PATH_ENVIRONMENT_VARIABLE}"""  # noqa: E501
        raise errors.ConfigFileNotFoundError(msg)

    current_directory = pathlib.Path.cwd()

    # Traverse upwards through the directory tree
    while current_directory != current_directory.parent:
        # Check if the configuration file exists
        config_file_absolute_path = current_directory / CONFIG_FILE

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


def _config_key(location: tuple[str | int, ...]) -> str:
    """Return a dotted configuration key from a validation location."""
    return ".".join(str(part) for part in location)


def _inherit_file_patterns(
    values: list[str],
    inherited: list[str],
) -> list[str]:
    """Append inherited file patterns without changing order or adding duplicates."""
    return list(dict.fromkeys((*values, *inherited)))


def _raise_config_validation_error(error: ValidationError) -> typing.NoReturn:
    """Translate a Pydantic validation error to a public configuration error."""
    detail = error.errors(include_url=False)[0]
    key = _config_key(detail["loc"])

    if detail["type"] == "missing":
        msg = f"Missing config key: {key}"
        raise errors.MissingConfigError(msg) from error

    value = detail.get("input")
    if detail["type"] == "model_type":
        message = "Expected a configuration section"
    elif detail["type"] == "value_error":
        # Pydantic prefixes custom ValueError messages with "Value error, ";
        # ctx["error"] holds the original, unprefixed message.
        message = str(detail["ctx"]["error"])
    else:
        message = detail["msg"]
    msg = f'Invalid config value for key "{key}": "{value}". {message}.'
    raise errors.InvalidConfigValueError(msg) from error


def parse_config(overrides: dict[str, object] | None = None) -> Config:
    """Parse config.

    Parameters:
    ----------
    overrides: dict[str, object] | None, optional
        Overrides applied on top of the user config.

    Returns:
    -------
    Config
        The parsed config.

    Raises:
    ------
    MissingConfigError
        Raised when a config is missing.
    InvalidConfigValueError
        Raised when a config value is invalid.
    """
    if not overrides:
        overrides = {}

    merged_config = _merge_config(overrides=overrides)

    try:
        config = Config.model_validate(merged_config)
    except ValidationError as error:
        _raise_config_validation_error(error)

    for section in (config.lint, config.format):
        section.include = _inherit_file_patterns(section.include, config.include)
        section.exclude = _inherit_file_patterns(section.exclude, config.exclude)

    return config
