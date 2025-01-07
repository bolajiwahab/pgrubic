# Linter

The pgrubic linter is a powerful tool designed to ensure your SQL files adhere to best practices and are free from common errors and mistakes.

## Running the linter

While the linter can used as a library, it is primarily intended to be used as a command-line tool. The linter can be run from the command line using the **`pgrubic lint`** command:

```bash
pgrubic lint                         # Lint SQL files in the current directory (and any subdirectories)
pgrubic lint .                       # Lint SQL files in the current directory (and any subdirectories)
pgrubic lint directory               # Lint SQL files in *directory* (and any subdirectories)
pgrubic lint directory/*.sql         # Lint SQL files in *directory*
pgrubic lint directory/file.sql      # Lint `file.sql` in *directory*
pgrubic lint file.sql                # Lint `file.sql`
pgrubic lint directory/*.sql --fix   # Lint SQL files in *directory* and fix fixable violations automatically
pgrubic lint file.sql --fix          # Lint `file.sql` and fix fixable violations automatically
```

## Controlling the selected rules

Rules can be enabled or disabled using the [**lint.select**](settings.md#select) and [**lint.ignore**](settings.md#ignore) settings. By default, all rules are enabled.

[**lint.select**](settings.md#select) and [**lint.ignore**](settings.md#ignore) can be combined in various ways to streamline rule selection. For example, the following configuration

<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
select = ["TP"]
ignore = ["TP015"]
```

</details>

will enable all the rules with the prefix `TP`, which falls under the [**typing**](rules.md/#typing-tp) category, with the exception of [**TP015**](../rules/typing/wrongly-typed-required-column).

When working with the default configuration, it is important to note that:

- Since all rules are enabled by default, it is recommended that you
explicitly enable the specific rules you want enabled since new rules would otherwise
be enabled by default when you upgrade
- [**lint.ignore**](settings.md#ignore) takes precedence over [**lint.select**](settings.md#select)

For the full list of all supported settings, see [**settings**](settings.md#lint).

## Fixing violations

There are linting rules whose violations the linter is able to fix on its own, these are called **fixable** violations. See [**Auto-fixable**](rules.md) to know whether a rule supports fixing.
for more about fixable violations.

to determine whether a rule supports fixing, see Rules

**Fix** mode is controlled via the [**fix**](settings.md#fix) setting and the command line flag `--fix`, with the flag taking precedence.

```bash
pgrubic lint --fix
```

Please note that fixes are formatted.

## Disabling fixes

Fixes can be enabled or disabled using the [**lint.fixable**](settings.md#fixable) and [**lint.unfixable**](settings.md#unfixable) settings. By default, all fixes are enabled. For example, the following configuration

<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[lint]
fixable = ["TP"]
unfixable = ["TP015"]
```

</details>

will enable fixes for all the rules with the prefix `TP`, which falls under the [**typing**](rules.md/#typing-tp) category, with the exception of [**TP015**](../rules/typing/wrongly-typed-required-column). Please note that **unfixable** takes precedence over **fixable**.

## Ignoring Violations

Similar to several other linters, the pgrubic linter provides various ways to ignore violations.

- To ignore a specific rule violation in a statement, add `-- noqa: {code}` directive to the top of the statement e.g `-- noqa: TP017`
- To ignore multiple rule violations in a statement, add `-- noqa: {code1}, {code2}, ...` directive to the top of the statement e.g `-- noqa: TP017, SM001`
- To ignore all violations in a statement, add `-- noqa` directive to the top of the statement
- To ignore a specific rule violation in a file, add `-- pgrubic: noqa: {code}` directive to the top of the file e.g `-- pgrubic: noqa: TP017`
- To ignore multiple rule violations in a file, add `-- pgrubic: noqa: {code1}, {code2}, ...` directive to the top of the file e.g `-- pgrubic: noqa: TP017, SM001`
- To ignore all violations in a file, use `-- pgrubic: noqa` directive to the top of the file
- To ignore a rule completely, add its code to [**lint.ignore**](settings.md#ignore) setting

See [**Rolling out**](tutorial.md#rolling-out) for additional resources on ignoring violations.

### Unused suppression comments

**pgrubic** will automatically warn about ununsed suppression comments.
