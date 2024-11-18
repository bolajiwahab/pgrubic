"""Test yaml test cases rules."""

import typing
import pathlib

import pytest

from tests import TEST_FILE
from pgrubic import core
from tests.conftest import update_config, load_test_cases


@pytest.mark.parametrize(
    ("test_id", "test_case"),
    load_test_cases(case="rule", directory=pathlib.Path("tests/fixtures/rules")),
)
def test_rules(
    linter_new: core.Linter,
    test_id: str,  # noqa: ARG001
    test_case: dict[str, str],
    capfd: typing.Any,
) -> None:
    """Test rules."""
    config_overrides: dict[str, typing.Any] = typing.cast(
        dict[str, typing.Any],
        test_case.get("config", {}),
    )

    # Apply overrides to global configuration
    update_config(linter_new.config, config_overrides)

    _ = linter_new.run(
        source_file=TEST_FILE,
        source_code=test_case["sql"],
    )

    out, _ = capfd.readouterr()
