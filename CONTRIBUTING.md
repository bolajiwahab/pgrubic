# Contributing
Thank you for your interest in contributing to Pgrubic!.
Contributions are welcome, whether they are bug reports, feature requests, code improvements, documentation updates, or new features. Contributions are welcome in form of Pull Requests. This guide will help you get started with the contributing process.

For significant changes, such as new rules, please consider creating an issue to outline your proposed feature for discussion.

## Getting Started
To contribute, you will need:

- Python 3.12 or higher.
- tox for running tests and other environments.

## Architecture
Pgrubic has two components:
1. The Linter - The linter loads the rules and check SQL files against the rules.
2. The Formatter - The formatter formats SQL files.

## Rules
There are currently 7 categories of rules:
- Constraint - Rules about constraints.
- General - Rules about general design practices.
- Naming - Rules about naming conventions.
- Schema - Rules about schemas.
- Security - Rules about security such as extensions and procedural languages.
- Typing - Rules about typing.
- Unsafe - Rules about unsafe migrations.

Rules use visitor pattern. This allows for traversing an Abstract Syntax Tree (AST) and applying specific checks at each node type. When implementing new rules, keep the following in mind:

- The rule should inherits from the base checker.
- Documentation is provided through the docstring of the rule.
- The rule should implement a set of particular named method(s), specifically `visit_XYZ` where XYZ is the name of the AST node it is visiting.
- The rule should add necessary violation to the violations list.
- Fixes must not have side effects, in the sense that such fixes should not trigger violation of another rule.

### Adding a new rule
To add a new rule, you need to:
1. Identify the right category of the rule.
2. The code of the rule should be the next number in the rule category e.g `GN030`
3. Create a file with a name matching the code of the rule e.g `GN030.py`, in `/pgrubic/src/pgrubic/core/rules/{category}` directory for the rule.
4. Inside the file, define a class with a name that explains the purpose of the rule e.g `MissingPrimaryKey`. This name will be used in the documentation so please keep it short and concise. The class should be inherits from the base checker.
5. Write detailed documentation in the docstring of the class.
6. Implement the visitor's method to visit the necessary AST node(s).
7. Add the violation of the rule to the violations list.
8. Implement fix to the rule if needed. The fix should not trigger violation of another rule.
9. Implement proper testing for the rule.
10. Update the generated documentation through:
```bash
tox -e docbuild
```

### Testing
Test files are located in `/pgrubic/tests/{category}` directory.
To test a rule, you need to:
1. Create a file with a name matching the code of the rule e.g `/pgrubic/tests/{category}/test_{rule_code}.py`.
2. Inside the file, write the necessary tests including violations and non-violations tests.
3. To run the tests, from the parent directory, use:
```
tox -e tests -- tests/{your_test_file}.py
```

## Formatter
Formatters are categorised into two:
- DDL - for DDL statements such as CREATE, ALTER, DROP, etc. These formatters are located in `/pgrubic/src/pgrubic/core/formatters/ddl/`.
- DML - for DML statements such as INSERT, UPDATE, etc. These formatters are located in `/pgrubic/src/pgrubic/core/formatters/dml/`.

### Adding a new formatter
To add a new formatter, you need to:
1. Identify the correct category.
2. Create a file with a name matching the statement tag e.g `create_table` for CREATE TABLE statement.
3. Inside the file, implement the formatter.
