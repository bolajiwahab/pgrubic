# Contributing

Thank you for your interest in contributing to pgrubic!.
Contributions are welcome, whether they are bug reports, feature requests, code improvements, documentation updates, or new features. Contributions are welcome in form of Pull Requests. This guide will help you get started with the contributing process.

For significant changes, such as new rules, please consider creating an [issue](https://github.com/bolajiwahab/pgrubic/issues) to outline your proposed feature for discussion.

## Development

To set up a development environment, you will need **tox**, **pre-commit**, and **python 3.12 or higher**.

1. Install **tox** and **pre-commit**:

    ```console
    python3.12 -m pip install --upgrade tox pre-commit
    ```

2. Create and activate a virtual environment:

    ```console
    tox -e dev --devenv .venv
    source .venv/bin/activate
    ```

3. Set up the git hook scripts

    ```console
    pre-commit install
    ```

## Project Structure

```text
.
├── src
    ├── pgrubic
        ├── core             # Core functionalities
        │   ├── cache.py     # Caching of formatted files
        │   ├── config.py    # Configuration
        |   ├── errors.py    # Errors
        │   ├── filters.py   # Sources filtering based on certain settings and `.sql` extension
        │   ├── logger.py    # Logger
        │   ├── loader.py    # Loading of rules
        │   ├── noqa.py      # noqa directive handling
        │   ├── linter.py    # Linter
        |   ├── formatter.py # Formatter
        │── formatters
        │   ├── ddl          # Formatters for DDL statements
        │   ├── dml          # Formatters for DML statements
        |── rules
        │   ├── constraint   # Rules about constraints
        │   ├── general      # Rules about general design practices
        │   ├── naming       # Rules about naming conventions
        │   ├── schema       # Rules about schemas
        │   ├── security     # Rules about security such as extensions and procedural languages
        │   ├── typing       # Rules about typing
        │   ├── unsafe       # Rules about unsafe migrations
│── docs                     # Documentation
│── tests                    # Tests
    │── fixtures             # Test fixtures
        │── rules            # Rule fixtures
        │── formatters       # Formatter fixtures
│── tools                    # Tools
│── pyproject.toml           # Pyproject file
```

## Architecture

pgrubic has two components:

1. **The Linter:** The linter loads the rules and check SQL files against the rules.
2. **The Formatter:** The formatter formats SQL files.

## Rules

There are currently 7 categories of rules:

1. **Constraint:** Rules about constraints.
2. **General:** Rules about general design practices.
3. **Naming:** Rules about naming conventions.
4. **Schema:** Rules about schemas.
5. **Security:** Rules about security such as extensions and procedural languages.
6. **Typing:** Rules about typing.
7. **Unsafe:** Rules about unsafe migrations.

Rules use visitor pattern. This allows for traversing an Abstract Syntax Tree (AST) and applying specific checks at each node type. When implementing new rules, keep the following in mind:

- The rule should inherit from the base checker
- Documentation is provided through the docstring of the rule
- The rule should implement a set of particular named method(s), specifically `visit_XYZ` where XYZ is the name of the AST node it is visiting. List of nodes can be found [here](https://pglast.readthedocs.io/en/latest/ast.html).
- The rule should add necessary violation to the violations list
- Fixes must not have side effects, in the sense that such fixes should not trigger violation of another rule

### Adding a new rule

To add a new rule, you need to:

1. Identify the right category of the rule.
2. The code of the rule should be the next number in the rule category e.g. `GN030`
3. Create a file with a name matching the code of the rule e.g. `GN030.py`, in `/pgrubic/src/pgrubic/core/rules/{category}` directory for the rule.
4. Inside the file, define a class with a name that explains the purpose of the rule e.g. `MissingPrimaryKey`. This name will be used in the documentation, so please keep it short and concise. The class should be inherited from the base checker.
5. Write detailed documentation in the docstring of the class.
6. Implement the visitor's method to visit the necessary AST node(s).
7. Add the violation of the rule to the violations list.
8. Implement fix to the rule if needed. The fix should not trigger violation of another rule.
9. Implement proper testing for the rule.
10. Update the generated documentation for rules through:

```bash
tox -e docbuild
```

### Testing

Test files are located in `/pgrubic/tests` directory.
To test a rule, you need to:

1. Create a fixture for the rule in e.g. `/pgrubic/tests/fixtures/rules/{rule_category}/{rule_code}.yml`.
2. Inside the file, write the necessary tests including, violations and non-violations tests.
3. To run the tests for all rules, use:

```bash
tox -e tests -- tests/test_rules.py
```

4. To run specific test, for example, use:

```bash
tox -e tests -- "tests/test_rules.py::test_rules[US028-US028_test_pass_concurrent_materialized_view_refresh-test_case767]"
```

## Formatter

Formatters are categorized into two:

1. **DDL:** for DDL statements such as CREATE, ALTER, DROP, etc. These formatters are located in `/pgrubic/src/pgrubic/core/formatters/ddl/`.
2. **DML:** for DML statements such as INSERT, UPDATE, etc. These formatters are located in `/pgrubic/src/pgrubic/core/formatters/dml/`.

We try to have a file per a specific object type such as table, index, etc.

### Adding a new formatter

To add a new formatter, you need to:

- Identify the correct category
- Create a new file with a name matching the object tag e.g. `table` or use the right existing file
- Inside the file, implement the formatter

### Testing

Test files are located in `/pgrubic/tests` directory.
To test a rule, you need to:

1. Create a fixture for the formatter in e.g. `/pgrubic/tests/fixtures/formatters/{rule_category}/{formatter}.yml`.
2. Inside the file, write the necessary tests, including the input SQL and expected output.
3. To run the tests for all formatters, use:

```bash
tox -e tests -- tests/test_formatters.py
```

4. To run specific test, for example, use:

```bash
tox -e tests -- "tests/test_formatters.py::test_formatters[VIEW-VIEW_drop_view-test_case94]"
```

## Documentation

To update the documentation, use:

```bash
tox -e docbuild
```

To preview changes to the documentation, from the parent directory, use:

```bash
mkdocs serve --config-file docs/mkdocs.yml
```

## Release

The project uses [commitizen](https://commitizen-tools.github.io/commitizen/) to manage releases. To create a new release, follow the steps below:

1. Prepare a new release by running

    ```bash
    tools/prepare_release.sh
    ```

    The above script automatically creates a branch named `Release`, runs `tox -e prepare-release` (which wraps around `cz bump`), and pushes the changes to the remote repository.

2. Create a pull request and get the changes merged

3. Push the tags, along with the latest tag

    ```bash
    git push origin --tags
    ```
