## Global

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
## Lint

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
## Format

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
