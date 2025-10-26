## 0.10.0 (2025-10-26)

### Feat

- build with python 3.14 (#164)

## 0.9.0 (2025-09-20)

### Feat

- **linter**: add lint report (#156)

### Fix

- **formatter**: handle new lines during errors (#157)

## 0.8.0 (2025-09-16)

### Feat

- **linter**: flag unsafe new column defaults (#151)
- **rule**: flag ordinal numbers in groupby and orderby (#141)
- **rule**: add rules for security definer functions (#140)

### Fix

- **linter**: flag new not-null column with volatile default (#150)
- **linter**: yoda condition operator fixes (#144)

## 0.7.0 (2025-08-12)

### Feat

- **linter**: linting of inline statements in plpgsql and function calls (#123)
- add support for skipping formatting of a whole file, simplify statements extraction, improve column offset for noqa directives (#108)

### Fix

- **linter**: ensure fixes are tracked on statement and file level, ensure unfixed statement are not discarded (#129)
- handle config errors (#126)
- generation of fixed source code when there are no fixes, extra new lines when we are unable to generate fixed source code or source code is unparseable (#125)

## 0.6.3 (2025-07-13)

### Fix

- **linter**: false-positive fixes caused by mismatched trailing newlines (#118)

## 0.6.2 (2025-07-06)

### Fix

- **linter**: reset ansi escape character sequence (#114)

## 0.6.1 (2025-06-15)

### Fix

- recaching of a source should not invalidate other sources already in the cache (#104)
- only apply fixes if there are duplicated columns in primary/unique keys (#101)

## 0.6.0 (2025-05-23)

### Feat

- implement graceful exit (#93)
- flag returning * (#86)

### Fix

- ignore semicolon in parentheses when building statement locations (#91)

## 0.5.3 (2025-03-23)

## 0.5.2 (2025-03-22)

## 0.5.1 (2025-03-22)

### Fix

- docker multi platform builds (#76)

## 0.5.0 (2025-02-20)

### Feat

- formatter for schema (#58)
- formatter for owner (#57)
- add formatter for function/procedure (#54)

## 0.4.0 (2025-01-31)

### Feat

- add rule for checking inline sql function body with wrong language (GN035) (#51)

### Fix

- enable all custom formatters (#52)

## 0.3.1 (2025-01-11)

### Fix

- fix release pipelines (#45)

## 0.3.0 (2025-01-11)

### Feat

- enable SM001 for DMLs except subqueries (#41)
- add docker images (#39)
- respect gitignore (#37)
- Parallelism (#36)

### Fix

- printing of empty lines from format diff (#40)

## 0.2.0 (2025-01-08)

### Feat

- add rule for typed table (#32)
- add rule for insert without target columns (#31)
- add rules to check for duplicate index, primary key, unique key columns (#29)
- add rule to check for stringified null (#27)

### Fix

- documentation, cleanup leftover backlog.md (#30)
- logo resolution (#28)

## 0.1.0 (2024-12-21)
