"""Test yaml test cases formatters."""

import typing
import pathlib

import yaml
import pytest

from tests import TEST_FILE
from pgrubic import core
from tests.conftest import update_config


def load_test_cases(directory: pathlib.Path) -> list[tuple[str, ...]]:
    """Load test cases from directory."""
    test_cases: list[tuple[str, ...]] = []

    for file in sorted(directory.rglob("*.yml"), key=lambda x: x.name):
        with file.open() as f:
            content: dict[str, typing.Any] = yaml.safe_load(f)

        formatter = content.pop("formatter")
        test_cases.extend((formatter + "_" + k, v) for k, v in content.items())
    return test_cases


@pytest.mark.parametrize(
    ("test_id", "test_case"),
    load_test_cases(pathlib.Path("tests/fixtures/formatters")),
)
def test_formatters(
    formatter: core.Formatter,
    test_id: str,
    test_case: dict[str, str],
) -> None:
    """Test formatters."""
    config_overrides: dict[str, typing.Any] = typing.cast(
        dict[str, typing.Any],
        test_case.get("config", {}),
    )

    # Apply overrides to configuration
    update_config(formatter.config, config_overrides)

    actual_output = formatter.format(
        source_file=TEST_FILE,
        source_code=test_case["sql"],
    )

    assert actual_output == test_case["expected"], f"Test failed: {test_id}"
