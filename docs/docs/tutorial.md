# Tutorial

This tutorial will guide you through the process of integrating pgrubic's linter and formatter into your project, both via CLI and as a library.

## Getting Started

## Installation

**pgrubic** can be installed using pip:

```console
pip install pgrubic
```

Please note **<span style="color:red">pgrubic is only supported on Python 3.12 or higher</span>**.

## Usage

We can use **pgrubic** from the command line to lint and format SQL files.
For example, say you have a project structure like the following:

```text
migrations
  └── sql
    └── V1__init.sql
```

where `V1__init.sql` contains the following SQL statements:

```sql
ALTER TABLE public.example ADD COLUMN bar boolean DEFAULT false NOT NULL;
ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

Let's run the pgrubic linter over the project with `pgrubic lint`:

```bash
pgrubic lint
migrations/V1__init.sql:2:39: TP017: Boolean field should not be nullable
2 | ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
                                          ^
Found 1 violation(s)
1 fix(es) available, 1 fix(es) enabled
```

**pgrubic** identified a **nullable** boolean field, which is most likely an oversight as boolean is either true or false. This is a fixable violation, so we can resolve the violation automatically by running `pgrubic check --fix`:

```bash
pgrubic lint --fix
Found 1 violation(s) (1 fixed, 0 remaining)
```

Checking **diff** with `git diff` produces the following:

```diff
--- a/V1__init.sql
+++ b/V1__init.sql
@@ -1,2 +1,4 @@
 ALTER TABLE public.example ADD COLUMN bar boolean DEFAULT false NOT NULL;
-ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
+
+ALTER TABLE public.example
+    ADD COLUMN foo boolean DEFAULT FALSE NOT NULL;
```

**pgrubic** runs in the current directory by default, but we can also give it specific paths:

```console
pgrubic lint migrations/V1__init.sql
```

We can also format our SQL with `pgrubic format`:

```console
pgrubic format

1 file(s) reformatted, 0 file(s) left unchanged
```

Checking **diff** with `git diff` produces the following:

```diff
--- a/V1__init.sql
+++ b/V1__init.sql
@@ -1,4 +1,5 @@
-ALTER TABLE public.example ADD COLUMN bar boolean DEFAULT false NOT NULL;
+ALTER TABLE public.example
+    ADD COLUMN bar boolean DEFAULT FALSE NOT NULL;

 ALTER TABLE public.example
     ADD COLUMN foo boolean DEFAULT FALSE NOT NULL;
```

So far, we have seen how to use **pgrubic** from the command line, but we can also use it as a library.
For example, say you have a python project structure like the following:

```text
migrations
  ├── __init__.py
  └── custom_linter.py
```

where `custom_linter.py` contains the following Python code:

```python
"""Custom linter."""

from pgrubic import core
from pgrubic.rules.typing import TP017


def check_for_nullable_boolean_field(source_file: str, source_code: str) -> None:
    """Linter for nullable boolean field."""
    config: core.Config = core.parse_config()

    linter: core.Linter = core.Linter(config=config, formatters=core.load_formatters)

    linter.checkers.add(TP017.NullableBooleanField())

    linting_result = linter.run(
        source_file=str(source_file),
        source_code=source_code,
    )

    linter.print_violations(
        violations=linting_result.violations,
        source_file=str(source_file),
    )


check_for_nullable_boolean_field(
    source_file="test.sql",
    source_code="ALTER TABLE public.example ADD COLUMN bar boolean DEFAULT false;",
)
```

## Configuration

We have been using the default configuration. The configuration can also be customized.

**pgrubic** uses **pgrubic.toml** file for configuration. For a more complete overview, see [Configuring pgrubic](configuration.md).

To override the default configuration, let's create `pgrubic.toml` in our project's root directory:

<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
required-columns = [
    { name = "foo", data-type = "text" }
]
```

</details>

Running **pgrubic** again, produces the following output:

```console
pgrubic lint
migrations/V1__init.sql:4:16: TP015: Column 'foo' expected type is 'text', found 'boolean'
4 |     ADD COLUMN foo boolean DEFAULT FALSE NOT NULL;
                   ^
Found 1 violation(s)
1 fix(es) available, 1 fix(es) enabled
```

For the full list of all supported settings, see [**settings**](settings.md).

### Selecting Rules

**pgrubic** supports [over 100 lint rules](rules.md) across **typing**, **general**, **constraint**, **unsafe migrations**, **naming**, **schema** and **security**. Please note that all rules are enabled by default.

If you are introducing the linter for the first time, you might want to streamline the set of rules that are enabled. In order to enable or disable specific rules, we can use [**lint.select**](settings.md#select) and [**lint.ignore**](settings.md#ignore) settings.
<details open>

<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
select = ["TP017"]
ignore = ["TP015"]
```

</details>

Running **pgrubic** again, produces the following output:

```console
pgrubic lint
Found 0 violation(s)
0 fix(es) available, 0 fix(es) enabled
```

Then over time, you may choose to enable additional rules.

### Ignoring violations

Every lint rule has a unique code and this code can be used to ignore violations of specific rule(s).

#### Ignore violations of single rule

A lint rule can be ignored by adding a `-- noqa: {rule_code}` comment to the violating SQL statement.
For example, to ignore violations of rule `TP017`, let's add a new file `migrations/V2__init.sql` with the following SQL statement:

```sql
ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

Let's also include `SM001` in the list of enabled rules in the `pgrubic.toml` config file.

<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
select = [
    "TP017",
    "SM001",
]
ignore = [
    "TP015",
]
```

</details>

Running **pgrubic**, produces the following output:

```console
pgrubic lint
migrations/V2__init.sql:1:13: SM001: Database object `example` should be schema qualified
1 | ALTER TABLE example ADD COLUMN foo boolean DEFAULT false;
                ^

/Users/bolajiwahab/repos/bolajiwahab/migrations/V2__init.sql:1:32: TP017: Boolean field should be not be nullable
1 | ALTER TABLE example ADD COLUMN foo boolean DEFAULT false;
                                   ^
Found 2 violation(s)
1 fix(es) available, 1 fix(es) enabled
```

To ignore the violation from `TP017`, let's add `-- noqa: TP017` to the SQL statement:

```sql
-- noqa: TP017
ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

Running **pgrubic** again, produces the following output:

```console
pgrubic lint
migrations/V2__init.sql:2:13: SM001: Database object `example` should be schema qualified
2 | ALTER TABLE example ADD COLUMN foo boolean DEFAULT false;
                ^
Found 1 violation(s)
0 fix(es) available, 0 fix(es) enabled
```

#### Ignoring violations of multiple lint rules

We can also ignore multiple lint rules at the same time. This is achieved by adding `-- noqa: {rule_code(s)}`, with the rule codes separated by a comma. For example,
`-- noqa: TP017, SM001`.

Let's also add the `SM001` to the `noqa` comment in the `migrations/V2__init.sql` file:

```sql
-- noqa: TP017, SM001
ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

Running **pgrubic** again, produces the following output:

```console
pgrubic lint
Found 0 violation(s)
0 fix(es) available, 0 fix(es) enabled
```

#### Ignoring all violations

To ignore all lint violations, we can add plain `-- noqa` to the SQL statement.
Let's update the `noqa` comment in the `migrations/V2__init.sql` file:

```sql
-- noqa
ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

Running **pgrubic** again, produces the following output:

```console
pgrubic lint
Found 0 violation(s)
0 fix(es) available, 0 fix(es) enabled
```

#### Ignoring violations in entire file

- To ignore all violations in a file for a specific rule, we can add `-- pgrubic: noqa: {rule_code}` to the beginning of the file
- To ignore all violations in a file for multiple rules, we can add `-- pgrubic: noqa: {rule_code(s)}` to the beginning of the file, with the rule codes separated by a comma. For example, `-- pgrubic: noqa: TP017, SM001`
- To ignore all violations in a file for all rules, we can add `-- pgrubic: noqa` to the beginning of the file

For more on ignoring violations, please see [Ignoring violations](linter.md#ignoring-violations).

## Rolling out

When introducing a new linter, most of the time, we may want to ignore all existing violations, especially on existing large codebases in order to streamline the roll-out process and instead focus on enforcing the linter going forward.

**pgrubic** supports this roll-out strategy via the command-line `--add-file-level-general-noqa` flag. When set, it will automatically add a `-- pgrubic: noqa` directive to the beginning of each SQL file to ignore all existing violations:

```console
pgrubic lint --add-file-level-general-noqa
File-level general noqa directive added to 1 file(s)
```

Checking **diff** with `git diff` produces the following:

```diff
--- a/V1__init.sql
+++ b/V1__init.sql
@@ -1,3 +1,4 @@
+-- pgrubic: noqa
 ALTER TABLE public.example
     ADD COLUMN bar boolean DEFAULT FALSE NOT NULL;
```

## Pre-commit

**pgrubic** comes with two pre-commit hooks:

- **pgrubic-lint**: lint changed files.
- **pgrubic-format**: format changed files.

Create a file named `.pre-commit-config.yaml` at the root of your git project. The file should look like this:

```yaml
- repo: https://github.com/bolajiwahab/pgrubic
  # The version of pgrubic to use.
  rev: 0.8.0
  hooks:
    - id: pgrubic-lint
    - id: pgrubic-format
```

To know more about pre-commit hooks, see [pre-commit](https://pre-commit.com/).

## Parallelism

**pgrubic** supports parallelism via the command-line `--workers` flag and the `PGRUBIC_WORKERS` environment variable,
with the flag when provided taking precedence over the environment variable while the environment variable takes precedence over the default number of workers (`4`).

**pgrubic** runs with the smallest of these values: the number of CPUs or the number of workers.

```bash
pgrubic lint --workers 4
pgrubic format --workers 4
```

With parallelism, **pgrubic** will run the linter and formatter concurrently on multiple processes. This can help speed up the process of linting and formatting.
