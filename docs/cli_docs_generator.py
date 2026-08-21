"""Generate CLI documentation from Click command metadata."""

import pathlib

from click import testing

from pgrubic import PACKAGE_NAME
from pgrubic.__main__ import cli

CLI_DOCUMENTATION = pathlib.Path.cwd() / "docs/docs/cli.md"
EXIT_CODES_HEADING = "## Exit codes"


def _render_help(*args: str) -> str:
    """Render plain CLI help for a command."""
    result = testing.CliRunner().invoke(
        cli,
        [*args, "--help"],
        prog_name=PACKAGE_NAME,
    )

    if result.exception:
        raise result.exception

    return "\n".join(line.rstrip() for line in result.output.rstrip().splitlines())


def main() -> None:
    """Generate CLI reference while preserving the exit-code documentation."""
    current_documentation = CLI_DOCUMENTATION.read_text()
    _, separator, exit_codes = current_documentation.partition(EXIT_CODES_HEADING)

    if not separator:
        msg = f"Missing {EXIT_CODES_HEADING!r} section in {CLI_DOCUMENTATION}"
        raise ValueError(msg)

    sections = [
        "# Command line interface",
        f"## {PACKAGE_NAME}\n\n```text\n{_render_help()}\n```",
        f"## lint\n\n```text\n{_render_help('lint')}\n```",
        f"## format\n\n```text\n{_render_help('format')}\n```",
        f"{EXIT_CODES_HEADING}{exit_codes.rstrip()}",
    ]
    CLI_DOCUMENTATION.write_text("\n\n".join(sections) + "\n")


if __name__ == "__main__":
    main()
