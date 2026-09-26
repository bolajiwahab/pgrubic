"""Test yaml test cases formatters."""

import typing
import pathlib

import pytest
from pglast import parser

from tests import TEST_FILE, conftest
from pgrubic import core


@pytest.mark.parametrize(
    ("test_formatter", "test_id", "test_case"),
    conftest.load_test_cases(
        test_case_type=conftest.TestCaseType.FORMATTER,
        path=pathlib.Path("tests/fixtures/formatters"),
    ),
)
def test_formatters(
    formatter: core.Formatter,
    test_formatter: str,
    test_id: str,
    test_case: dict[str, str],
) -> None:
    """Test formatters."""
    config_overrides: dict[str, typing.Any] = typing.cast(
        dict[str, typing.Any],
        test_case.get("config", {}),
    )

    with conftest.update_config(config=formatter.config, overrides=config_overrides):
        result = formatter.format(
            source_file=TEST_FILE,
            source_code=test_case["sql"],
        )

        assert result.formatted_source_code == test_case["expected"], (
            f"Test failed for formatter: `{test_formatter}` in `{test_id}`"
        )

        idempotent_result = formatter.format(
            source_file=TEST_FILE,
            source_code=result.formatted_source_code,
        )
        assert idempotent_result.formatted_source_code == result.formatted_source_code, (
            f"Formatter is not idempotent: `{test_formatter}` in `{test_id}`"
        )

        skip_semantic_check = test_case.get("skip_semantic_check")
        if skip_semantic_check is not None:
            assert isinstance(skip_semantic_check, str), (
                "skip_semantic_check must specify a reason: "
                f"`{test_formatter}` in `{test_id}`"
            )
            assert skip_semantic_check.strip(), (
                "skip_semantic_check must specify a non-empty reason: "
                f"`{test_formatter}` in `{test_id}`"
            )

        # reformat the formatted source code to ensure it is valid and idempotent
        try:
            reformat_result = formatter.format(
                source_file=TEST_FILE,
                source_code=result.formatted_source_code,
            )

            assert (
                reformat_result.formatted_source_code == result.formatted_source_code
            ), f"Formatter is not idempotent: `{test_formatter}` in `{test_id}`"
        except parser.ParseError as error:
            msg = f"Formatted code is not a valid syntax: {error!s}"
            raise ValueError(msg) from error
