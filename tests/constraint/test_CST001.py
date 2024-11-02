"""Test cascade update."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.constraint.CT001 import CascadeUpdate


@pytest.fixture(scope="module")
def cascade_update() -> core.BaseChecker:
    """Create an instance of CascadeUpdate."""
    core.add_apply_fix_to_rule(CascadeUpdate)
    core.add_set_locations_to_rule(CascadeUpdate)
    return CascadeUpdate()


@pytest.fixture
def lint_cascade_update(
    linter: core.Linter,
    cascade_update: core.BaseChecker,
) -> core.Linter:
    """Lint CascadeUpdate."""
    cascade_update.config.lint.fix = False
    linter.checkers.add(cascade_update)

    return linter


def test_cascade_update_rule_code(cascade_update: core.BaseChecker) -> None:
    """Test cascade update rule code."""
    assert cascade_update.code == cascade_update.__module__.split(".")[-1]


def test_cascade_update_auto_fixable(cascade_update: core.BaseChecker) -> None:
    """Test cascade update auto fixable."""
    assert cascade_update.is_auto_fixable is True


def test_pass_on_update_no_action(lint_cascade_update: core.Linter) -> None:
    """Test fail cascade update."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON UPDATE NO ACTION
    );
    """

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_on_update_restrict(lint_cascade_update: core.Linter) -> None:
    """Test fail cascade update."""
    sql_fail: str = """
    ALTER TABLE books
        ADD CONSTRAINT distfk
            FOREIGN KEY (author_id) REFERENCES authors (author_id) ON UPDATE RESTRICT
    ;
    """

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_on_update_set_null(lint_cascade_update: core.Linter) -> None:
    """Test fail cascade update."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON UPDATE SET NULL
    );
    """

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_on_update_set_default(lint_cascade_update: core.Linter) -> None:
    """Test fail cascade update."""
    sql_fail: str = """
    ALTER TABLE books
        ADD CONSTRAINT distfk
            FOREIGN KEY (author_id) REFERENCES authors (author_id) ON UPDATE SET DEFAULT
    ;
    """

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_cascade_update(lint_cascade_update: core.Linter) -> None:
    """Test fail create table cascade update."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON UPDATE CASCADE
    );
    """

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_cascade_update(lint_cascade_update: core.Linter) -> None:
    """Test fail alter table cascade update."""
    sql_fail: str = """
    ALTER TABLE books
        ADD CONSTRAINT distfk
            FOREIGN KEY (author_id) REFERENCES authors (author_id) ON UPDATE CASCADE
    ;
    """

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_cascade_update_description(
    lint_cascade_update: core.Linter,
    cascade_update: core.BaseChecker,
) -> None:
    """Test fail cascade update description."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON UPDATE CASCADE
    );
    """

    _: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(iter(cascade_update.violations)).description
        == "Cascade update in foreign key constraint"
    )


def test_pass_noqa_cascade_update(lint_cascade_update: core.Linter) -> None:
    """Test pass noqa cascade update."""
    sql_pass_noqa: str = """
    -- noqa: CT001
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON UPDATE CASCADE
    );
    """

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_cascade_update(lint_cascade_update: core.Linter) -> None:
    """Test fail noqa cascade update."""
    sql_noqa: str = """
    -- noqa: CST003
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON UPDATE CASCADE
    );
    """

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_cascade_update(
    lint_cascade_update: core.Linter,
) -> None:
    """Test fail noqa cascade update."""
    sql_noqa: str = """
    -- noqa
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON UPDATE CASCADE
    );
    """

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_cascade_update(
    lint_cascade_update: core.Linter,
    cascade_update: core.BaseChecker,
) -> None:
    """Test fail fix create table cascade update."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON UPDATE CASCADE
    );
    """

    sql_fix: str = "CREATE TABLE books (\n    author_id integer REFERENCES authors (author_id) ON UPDATE RESTRICT\n);\n"  # noqa: E501

    cascade_update.config.lint.fix = True

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_cascade_update(
    lint_cascade_update: core.Linter,
    cascade_update: core.BaseChecker,
) -> None:
    """Test fail fix alter table cascade update."""
    sql_fail: str = """
    ALTER TABLE books
        ADD CONSTRAINT distfk
            FOREIGN KEY (author_id) REFERENCES authors (author_id) ON UPDATE CASCADE
    ;
    """

    sql_fix: str = "ALTER TABLE books\n    ADD CONSTRAINT distfk FOREIGN KEY (author_id) REFERENCES authors (author_id) ON UPDATE RESTRICT;\n"  # noqa: E501

    cascade_update.config.lint.fix = True

    violations: core.ViolationMetric = lint_cascade_update.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
