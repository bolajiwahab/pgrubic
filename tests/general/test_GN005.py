"""Test for index elements more than three."""

import pytest

from tests import SOURCE_PATH
from pgrubic import core
from pgrubic.rules.general.GN005 import IndexElementsMoreThanThree


@pytest.fixture(scope="module")
def index_elements_more_than_three() -> core.BaseChecker:
    """Create an instance of IndexElementsMoreThanThree."""
    core.add_set_locations_to_rule(IndexElementsMoreThanThree)
    return IndexElementsMoreThanThree()


@pytest.fixture
def lint_index_elements_more_than_three(
    linter: core.Linter,
    index_elements_more_than_three: core.BaseChecker,
) -> core.Linter:
    """Lint IndexElementsMoreThanThree."""
    linter.checkers.add(index_elements_more_than_three)

    return linter


def test_index_elements_more_than_three_rule_code(
    index_elements_more_than_three: core.BaseChecker,
) -> None:
    """Test index elements more than three rule code."""
    assert (
        index_elements_more_than_three.code
        == index_elements_more_than_three.__module__.split(".")[-1]
    )


def test_index_elements_more_than_three_auto_fixable(
    index_elements_more_than_three: core.BaseChecker,
) -> None:
    """Test index elements more than three auto fixable."""
    assert index_elements_more_than_three.is_auto_fixable is False


def test_pass_index_elements_not_more_than_three(
    lint_index_elements_more_than_three: core.Linter,
) -> None:
    """Test fail index elements more than three."""
    sql_fail: str = "CREATE INDEX music_age_idx ON music (age);"

    violations: core.ViolationMetric = lint_index_elements_more_than_three.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_index_elements_more_than_three(
    lint_index_elements_more_than_three: core.Linter,
) -> None:
    """Test fail index elements more than three."""
    sql_fail: str = (
        "CREATE INDEX music_id_age_name_email_idx ON music (id, age, name, email);"
    )

    violations: core.ViolationMetric = lint_index_elements_more_than_three.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_fail_index_elements_more_than_three_description(
    lint_index_elements_more_than_three: core.Linter,
    index_elements_more_than_three: core.BaseChecker,
) -> None:
    """Test index elements more than three description."""
    sql_fail: str = (
        "CREATE INDEX music_id_age_name_email_idx ON music (id, age, name, email);"
    )

    _: core.ViolationMetric = lint_index_elements_more_than_three.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail,
    )

    assert (
        next(
            iter(index_elements_more_than_three.violations),
        ).description
        == "Index elements more than 3"
    )


def test_pass_noqa_index_elements_more_than_three(
    lint_index_elements_more_than_three: core.Linter,
) -> None:
    """Test pass noqa index elements more than three."""
    sql_pass_noqa: str = """
    -- noqa: GN005
    CREATE INDEX music_id_age_name_email_idx ON music (id, age, name, email);
    """

    violations: core.ViolationMetric = lint_index_elements_more_than_three.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )


def test_fail_noqa_index_elements_more_than_three(
    lint_index_elements_more_than_three: core.Linter,
) -> None:
    """Test fail noqa index elements more than three."""
    sql_fail_noqa: str = """
    -- noqa: GN001
    CREATE INDEX music_id_age_name_email_idx ON music (id, age, name, email);
    """

    violations: core.ViolationMetric = lint_index_elements_more_than_three.run(
        source_path=SOURCE_PATH,
        source_code=sql_fail_noqa,
    )

    assert violations == core.ViolationMetric(
        total=1,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=1,
    )


def test_pass_general_noqa_index_elements_more_than_three(
    lint_index_elements_more_than_three: core.Linter,
) -> None:
    """Test fail noqa index elements more than three."""
    sql_pass_noqa: str = """
    -- noqa:
    CREATE INDEX music_id_age_name_email_idx ON music (id, age, name, email);
    """

    violations: core.ViolationMetric = lint_index_elements_more_than_three.run(
        source_path=SOURCE_PATH,
        source_code=sql_pass_noqa,
    )

    assert violations == core.ViolationMetric(
        total=0,
        fixed_total=0,
        fixable_auto_total=0,
        fixable_manual_total=0,
    )
