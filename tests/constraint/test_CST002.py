"""Test cascade update."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.constraint.CT002 import CascadeDelete


@pytest.fixture(scope="module")
def cascade_delete() -> core.BaseChecker:
    """Create an instance of CascadeDelete."""
    core.add_apply_fix_to_rule(CascadeDelete)
    return CascadeDelete()


@pytest.fixture
def lint_cascade_delete(
    linter: core.Linter,
    cascade_delete: core.BaseChecker,
) -> core.Linter:
    """Lint CascadeDelete."""
    cascade_delete.config.lint.fix = False
    linter.checkers.add(cascade_delete)

    return linter


def test_cascade_delete_rule_code(cascade_delete: core.BaseChecker) -> None:
    """Test cascade update rule code."""
    assert cascade_delete.code == cascade_delete.__module__.split(".")[-1]


def test_cascade_delete_auto_fixable(cascade_delete: core.BaseChecker) -> None:
    """Test cascade update auto fixable."""
    assert cascade_delete.is_auto_fixable is True


def test_pass_on_delete_no_action(lint_cascade_delete: core.Linter) -> None:
    """Test fail cascade update."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON DELETE NO ACTION
    );
    """

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_on_delete_restrict(lint_cascade_delete: core.Linter) -> None:
    """Test fail cascade update."""
    sql_fail: str = """
    ALTER TABLE books
        ADD CONSTRAINT distfk
            FOREIGN KEY (author_id) REFERENCES authors (author_id) ON DELETE RESTRICT
    ;
    """

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_on_delete_set_null(lint_cascade_delete: core.Linter) -> None:
    """Test fail cascade update."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON DELETE SET NULL
    );
    """

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_on_delete_set_default(lint_cascade_delete: core.Linter) -> None:
    """Test fail cascade update."""
    sql_fail: str = """
    ALTER TABLE books
        ADD CONSTRAINT distfk
            FOREIGN KEY (author_id) REFERENCES authors (author_id) ON DELETE SET DEFAULT
    ;
    """

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_cascade_delete(lint_cascade_delete: core.Linter) -> None:
    """Test fail create table cascade update."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON DELETE CASCADE
    );
    """

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_cascade_delete(lint_cascade_delete: core.Linter) -> None:
    """Test fail alter table cascade update."""
    sql_fail: str = """
    ALTER TABLE books
        ADD CONSTRAINT distfk
            FOREIGN KEY (author_id) REFERENCES authors (author_id) ON DELETE CASCADE
    ;
    """

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_cascade_delete_description(
    lint_cascade_delete: core.Linter,
    cascade_delete: core.BaseChecker,
) -> None:
    """Test fail cascade update description."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON DELETE CASCADE
    );
    """

    _: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(iter(cascade_delete.violations)).description
        == "Cascade delete in foreign key constraint"
    )


def test_pass_noqa_cascade_delete(lint_cascade_delete: core.Linter) -> None:
    """Test pass noqa cascade update."""
    sql_pass_noqa: str = """
    -- noqa: CT002
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON DELETE CASCADE
    );
    """

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_cascade_delete(lint_cascade_delete: core.Linter) -> None:
    """Test fail noqa cascade update."""
    sql_noqa: str = """
    -- noqa: CST003
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON DELETE CASCADE
    );
    """

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_cascade_delete(
    lint_cascade_delete: core.Linter,
) -> None:
    """Test fail noqa cascade update."""
    sql_noqa: str = """
    -- noqa:
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON DELETE CASCADE
    );
    """

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_cascade_delete(
    lint_cascade_delete: core.Linter,
    cascade_delete: core.BaseChecker,
) -> None:
    """Test fail fix create table cascade update."""
    sql_fail: str = """
    CREATE TABLE books (
        author_id INT REFERENCES authors(author_id) ON DELETE CASCADE
    );
    """

    sql_fix: str = (
        "CREATE TABLE books (\n  author_id integer REFERENCES authors (author_id) ON DELETE RESTRICT\n);"  # noqa: E501
    )

    cascade_delete.config.lint.fix = True

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )


def test_fail_fix_alter_table_cascade_delete(
    lint_cascade_delete: core.Linter,
    cascade_delete: core.BaseChecker,
) -> None:
    """Test fail fix alter table cascade update."""
    sql_fail: str = """
    ALTER TABLE books
        ADD CONSTRAINT distfk
            FOREIGN KEY (author_id) REFERENCES authors (author_id) ON DELETE CASCADE
    ;
    """

    sql_fix: str = (
        "ALTER TABLE books ADD CONSTRAINT distfk FOREIGN KEY (author_id) REFERENCES authors (author_id) ON DELETE RESTRICT;"  # noqa: E501
    )

    cascade_delete.config.lint.fix = True

    violations: core.ViolationMetric = lint_cascade_delete.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=1,
        fixable_auto_total=1,
        fixable_manual_total=0,
        fix=sql_fix,
    )
