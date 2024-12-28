# Tutorial

This tutorial will guide you through the process of integrating pgrubic's linter and formatter into your project, both via CLI and as a library with a direct API for custom usage.

## Getting Started

## Installation
```console
pip install pgrubic
```
**<span style="color:red">Pgrubic is only supported on Python 3.12+</span>**.

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

```console
$ pgrubic lint
migrations/V1__init.sql:2:39: TP017: Boolean field should not be nullable
2 | ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
                                          ^
Found 1 violation(s)
1 fix(es) available
```

**pgrubic** identified a **nullable** boolean field, which is most likely an oversight as boolean is either true or false. This is a fixable violation, so we can resolve the violation automatically by running `pgrubic check --fix`:

```console
$ pgrubic lint --fix
Found 1 violation(s) (1 fixed, 0 remaining)
```

Checking diff with `git diff` produces the following:

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

**pgrubic** runs in the current directory by default, but we can also pass specific paths to it:

```console
$ pgrubic lint migrations/V1__init.sql
```

We can also format our SQL with `pgrubic format`:

```console
$ pgrubic format

1 file(s) reformatted
```

Checking diff with `git diff` produces the following:

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

    core.BaseChecker.config = config

    core.add_set_locations_to_rule(TP017.NullableBooleanField)
    core.add_apply_fix_to_rule(TP017.NullableBooleanField)

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

**pgrubic** can be configured via the `pgrubic.toml` file in either the current directory or in the user's home directory. For a more complete overview, see [_Configuring pgrubic_](configuration.md).

**pgrubic** uses **pgrubic.toml** file for configuration.

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
$ pgrubic lint
migrations/V1__init.sql:4:16: TP015: Column 'foo' expected type is 'text', found 'boolean'
4 |     ADD COLUMN foo boolean DEFAULT FALSE NOT NULL;
                   ^
Found 1 violation(s)
1 fix(es) available
```

For the full list of all supported settings, see [_Settings_](settings.md).
### Rule Selection

**pgrubic** supports [over 100 lint rules](rules.md) across **typing**, **general**, **constraint**, **unsafe migrations**, **naming**, **schema** and **security**. All rules are enabled by default.

If you are introducing the linter for the first time, you might want to streamline the set of rules that are enabled. In order to select/deselect specific rules, we can use the `select` or `ignore` option in the `[lint]` section of the `pgrubic.toml` config file.
<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
select = [
    "TP017",
]
ignore = [
    "TP015",
]
```
</details>

Running **pgrubic** again, produces the following output:

```console
$ pgrubic lint
Found 0 violation(s)
0 fix(es) available
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
$ pgrubic lint
migrations/V2__init.sql:1:13: SM001: Database object `example` should be schema qualified
1 | ALTER TABLE example ADD COLUMN foo boolean DEFAULT false;
                ^

/Users/bolajiwahab/repos/bolajiwahab/migrations/V2__init.sql:1:32: TP017: Boolean field should be not be nullable
1 | ALTER TABLE example ADD COLUMN foo boolean DEFAULT false;
                                   ^
Found 2 violation(s)
1 fix(es) available
```

To ignore the violation from `TP017`, let's add `-- noqa: TP017` to the SQL statement:

```sql
-- noqa: TP017
ALTER TABLE public.example ADD COLUMN foo boolean DEFAULT false;
```

Running **pgrubic** again, produces the following output:

```console
$ pgrubic lint
migrations/V2__init.sql:2:13: SM001: Database object `example` should be schema qualified
2 | ALTER TABLE example ADD COLUMN foo boolean DEFAULT false;
                ^
Found 1 violation(s)
0 fix(es) available
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
$ pgrubic lint
Found 0 violation(s)
0 fix(es) available
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
$ pgrubic lint
Found 0 violation(s)
0 fix(es) available
```

#### Ignoring violations in entire file
- To ignore all violations in a file for a specific rule, we can add `-- pgrubic: noqa: {rule_code}` to the beginning of the file.
- To ignore all violations in a file for multiple rules, we can add `-- pgrubic: noqa: {rule_code(s)}` to the beginning of the file, with the rule codes separated by a comma. For example, `-- pgrubic: noqa: TP017, SM001`.
- To ignore all violations in a file for all rules, we can add `-- pgrubic: noqa` to the beginning of the file.

For further instructions on ignoring violations, please see [_Ignoring violations_](linter.md#ignoring-violations).