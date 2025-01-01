# Command line interface

## pgrubic

  PostgreSQL linter and formatter for schema migrations and design
  best practices.

### **Options**

#### **--version**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Show the version and exit.

  Examples:

     pgrubic lint

     pgrubic lint .

     pgrubic lint *.sql

     pgrubic lint example.sql

     pgrubic format file.sql

     pgrubic format migrations/

## **lint**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Lint SQL files.

### **Options**

#### **--fix**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Fix lint violations automatically.

#### **--ignore-noqa**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Whether to ignore noqa directives.

#### **--add-file-level-general-noqa**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Whether to add file-level noqa directives.

#### **--verbose**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Enable verbose logging.

## **format**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Format SQL files.

### **Options**

#### **--check**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Check if any files would have been modified.

#### **--diff**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Report the difference between the current file and how the
formatted file would look like.

#### **--no-cache**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Whether to read the cache.

#### **--verbose**

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Enable verbose logging.

## Exit codes

When using **pgrubic** as a command line tool, it returns [exit-code](https://shapeshed.com/unix-exit-codes/) which can be useful in CI pipelines.

### lint

| Code | Description                                                    |
| ---- | -------------------------------------------------------------- |
| 0    | No violations found or all violations were fixed automatically |
| 1    | Violations found                                               |
| 2    | Error occurred during linting                                  |

### format

| Code |                    Description                          |
| ---- | --------------------------------------------------------|
| 0    | Formatting was successful, even if no changes were made |
| 2    | Error occurred during formatting                        |

#### --check

| Code |           Description            |
| -----| ---------------------------------|
| 0    | No changes would be made         |
| 1    | Changes would be made            |
| 2    | Error occurred during formatting |

#### --diff

| Code |           Description            |
| ---- | ---------------------------------|
| 0    | No changes would be made         |
| 1    | Changes would be made            |
| 2    | Error occurred during formatting |
