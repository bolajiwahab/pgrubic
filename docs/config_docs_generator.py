"""Synchronize documented default configuration with the packaged TOML file."""

import pathlib

DEFAULT_CONFIG = pathlib.Path.cwd() / "src/pgrubic/pgrubic.toml"

DOCUMENTATION = (
    pathlib.Path.cwd() / "README.md",
    pathlib.Path.cwd() / "docs/docs/configuration.md",
)

START_MARKER = "<!-- BEGIN GENERATED DEFAULT CONFIG -->"
END_MARKER = "<!-- END GENERATED DEFAULT CONFIG -->"


def _generate_config_block() -> str:
    """Generate the default configuration block."""
    return (
        f"{START_MARKER}\n\n"
        f"```toml\n{DEFAULT_CONFIG.read_text().strip()}\n```\n\n"
        f"{END_MARKER}"
    )


def _sync_documentation(path: pathlib.Path) -> None:
    """Replace a marked default-configuration block."""
    content = path.read_text()

    if START_MARKER in content:
        start = content.index(START_MARKER)
        end = content.index(END_MARKER, start) + len(END_MARKER)
    else:
        anchor = (
            "The following configuration options"
            if path.name == "README.md"
            else "## Default Configuration"
        )
        start = content.index("```toml", content.index(anchor))
        end = content.index("```", start + len("```toml")) + len("```")

    path.write_text(content[:start] + _generate_config_block() + content[end:])


def main() -> None:
    """Synchronize every documented copy of the default configuration."""
    for path in DOCUMENTATION:
        _sync_documentation(path)


if __name__ == "__main__":
    main()
