"""Test special character in identifier."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.naming.NM012 import SpecialCharacterInIdentifier


@pytest.fixture(scope="module")
def special_character_in_identifier() -> core.BaseChecker:
    """Create an instance of special character in identifier."""
    core.add_set_locations_to_rule(SpecialCharacterInIdentifier)
    return SpecialCharacterInIdentifier()


@pytest.fixture
def lint_special_character_in_identifier(
    linter: core.Linter,
    special_character_in_identifier: core.BaseChecker,
) -> core.Linter:
    """Lint special character in identifier."""
    linter.checkers.add(special_character_in_identifier)

    return linter


def test_special_character_in_identifier_rule_code(
    special_character_in_identifier: core.BaseChecker,
) -> None:
    """Test special character in identifier rule code."""
    assert (
        special_character_in_identifier.code
        == special_character_in_identifier.__module__.split(".")[-1]
    )


def test_special_character_in_identifier_auto_fixable(
    special_character_in_identifier: core.BaseChecker,
) -> None:
    """Test special character in identifier auto fixable."""
    assert special_character_in_identifier.is_auto_fixable is False


def test_fail_special_character_in_identifier(
    lint_special_character_in_identifier: core.Linter,
) -> None:
    """Test fail special character in identifier."""
    sql_fail: str = "SELECT INTO tbl$ FROM tbl;"

    violations: core.ViolationMetric = lint_special_character_in_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_special_character_in_identifier_description(
    lint_special_character_in_identifier: core.Linter,
    special_character_in_identifier: core.BaseChecker,
) -> None:
    """Test special character in identifier description."""
    sql_fail: str = "CREATE RULE notify$_me AS ON UPDATE TO tbl DO ALSO NOTIFY mytable;"

    _: core.ViolationMetric = lint_special_character_in_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(special_character_in_identifier.violations),
        ).description
        == "Special characters in identifier `notify$_me`"
    )


def test_pass_noqa_special_character_in_identifier(
    lint_special_character_in_identifier: core.Linter,
) -> None:
    """Test pass noqa special character in identifier."""
    sql_pass_noqa: str = """
    -- noqa: NM012
    CREATE TYPE mo$od AS ENUM ('sad', 'ok', 'happy');
    """

    violations: core.ViolationMetric = lint_special_character_in_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_special_character_in_identifier(
    lint_special_character_in_identifier: core.Linter,
) -> None:
    """Test fail noqa special character in identifier."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE TRIGGER auto_$inserter
    AFTER INSERT ON A
    FOR EACH ROW
    EXECUTE PROCEDURE auto_insert();
    """

    violations: core.ViolationMetric = lint_special_character_in_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_special_character_in_identifier(
    lint_special_character_in_identifier: core.Linter,
) -> None:
    """Test pass noqa special character in identifier."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE INDEX "INDEX" ON tbl (col);
    """

    violations: core.ViolationMetric = lint_special_character_in_identifier.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
