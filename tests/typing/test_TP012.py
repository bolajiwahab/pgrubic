"""Test usage of xml."""

import pytest

from tests import TEST_FILE
from pgrubic import core
from pgrubic.rules.typing.TP012 import Xml


@pytest.fixture(scope="module")
def xml() -> core.BaseChecker:
    """Create an instance of xml."""
    core.add_apply_fix_to_rule(Xml)
    core.add_set_locations_to_rule(Xml)
    return Xml()


@pytest.fixture
def lint_xml(
    linter: core.Linter,
    xml: core.BaseChecker,
) -> core.Linter:
    """Lint xml."""
    xml.config.lint.fix = False
    linter.checkers.add(xml)

    return linter


def test_xml_rule_code(
    xml: core.BaseChecker,
) -> None:
    """Test xml rule code."""
    assert xml.code == xml.__module__.split(".")[-1]


def test_xml_auto_fixable(
    xml: core.BaseChecker,
) -> None:
    """Test xml auto fixable."""
    assert xml.is_auto_fixable is True


def test_pass_create_table_xmlb(
    lint_xml: core.Linter,
) -> None:
    """Test pass jsonb."""
    sql_fail: str = "CREATE TABLE tbl (details jsonb);"

    violations: core.ViolationMetric = lint_xml.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_pass_alter_table_xmlb(
    lint_xml: core.Linter,
) -> None:
    """Test pass jsonb."""
    sql_fail: str = """
    ALTER TABLE tbl ADD COLUMN details jsonb;
    """

    violations: core.ViolationMetric = lint_xml.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_create_table_xml(
    lint_xml: core.Linter,
) -> None:
    """Test fail create table xml."""
    sql_fail: str = "CREATE TABLE tbl (details xml);"

    violations: core.ViolationMetric = lint_xml.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_alter_table_xml(
    lint_xml: core.Linter,
) -> None:
    """Test fail alter table xml."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN details xml;"

    violations: core.ViolationMetric = lint_xml.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_fail_xml_description(
    lint_xml: core.Linter,
    xml: core.BaseChecker,
) -> None:
    """Test xml description."""
    sql_fail: str = "CREATE TABLE tbl (details xml);"

    _: core.ViolationMetric = lint_xml.run(
        source_file=TEST_FILE,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(xml.violations),
        ).description
        == "Prefer jsonb over xml"
    )


def test_pass_noqa_xml(
    lint_xml: core.Linter,
) -> None:
    """Test pass noqa xml."""
    sql_pass_noqa: str = """
    -- noqa: TP012
    CREATE TABLE tbl (tbl_id int, details xml);
    """

    violations: core.ViolationMetric = lint_xml.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_xml(
    lint_xml: core.Linter,
) -> None:
    """Test fail noqa xml."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    ALTER TABLE tbl ADD COLUMN details xml;
    """

    violations: core.ViolationMetric = lint_xml.run(
        source_file=TEST_FILE,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=1,
        fixable_manual_total=0,
    )


def test_pass_general_noqa_xml(
    lint_xml: core.Linter,
) -> None:
    """Test pass noqa xml."""
    sql_pass_noqa: str = """
    -- noqa
    CREATE TABLE tbl (tbl_id int, details xml);
    """

    violations: core.ViolationMetric = lint_xml.run(
        source_file=TEST_FILE,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_fix_create_table_xml(
    lint_xml: core.Linter,
    xml: core.BaseChecker,
) -> None:
    """Test fail fix xml."""
    sql_fail: str = "CREATE TABLE tbl (user_id int, details xml);"

    sql_fix: str = "CREATE TABLE tbl (\n    user_id integer\n  , details jsonb\n);\n"

    xml.config.lint.fix = True

    violations: core.ViolationMetric = lint_xml.run(
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


def test_fail_fix_alter_table_xml(
    lint_xml: core.Linter,
    xml: core.BaseChecker,
) -> None:
    """Test fail fix xml."""
    sql_fail: str = "ALTER TABLE tbl ADD COLUMN details xml;"

    sql_fix: str = "ALTER TABLE tbl\n    ADD COLUMN details jsonb;\n"

    xml.config.lint.fix = True

    violations: core.ViolationMetric = lint_xml.run(
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
