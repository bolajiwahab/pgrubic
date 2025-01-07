# Formatter

The core principle of the pgrubic formatter is to make SQL statements easy to read, easy to maintain, less prone to error and beautiful to see. The formatter is opinionated with few configuration options.

## Components

There are two components of the formatter:

- **DDL**: Designed to be almost identical with **pg_dump** styling, with differences on subcommands.
- **DML**: Designed to produce **river** style.

## Runing the formatter

While the formatter can used as a library, it is primarily intended to be used as a command-line tool. The linter can be run from the command line using the **`pgrubic format`** command:

```bash
pgrubic format                         # Format SQL files in the current directory (and any subdirectories)
pgrubic format .                       # Format SQL files in the current directory (and any subdirectories)
pgrubic format directory               # Format SQL files in *directory* (and any subdirectories)
pgrubic format directory/*.sql         # Format SQL files in *directory*
pgrubic format directory/file.sql      # Format `file.sql` in *directory*
pgrubic format file.sql                # Format `file.sql`
```

## Configuration

The formatter is opinionated, with few configuration options. For example, the following configuration

<details open>
<summary><strong>pgrubic.toml</strong></summary>

```toml
[format]
comma-at-beginning = true
```

</details>

will add comma as a prefix as opposed to a suffix when formatting a list of
items, such as list of columns in which each column is on a separate line.

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

For the full list of all supported settings, see [**settings**](settings.md#format).

## Skipping formatting

Similar to several other formatters, the pgrubic formatter provides various ways to skip formatting a statement/file.

- To skip formatting a statement, add `-- fmt: skip` directive to the top of the statement
- To skip formatting a file completely, add the file name to the [**format.exclude**](settings.md/#exclude_2) setting
