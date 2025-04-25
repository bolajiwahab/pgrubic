"""Generate documentation for settings."""

import typing
import pathlib

from pgrubic import core

categories: dict[str, object] = {
    "Global": core.config.Config,
    "Lint": core.config.Lint,
    "Format": core.config.Format,
}

settings = pathlib.Path.cwd() / "docs/docs/settings.md"

# remove existing documentation
settings.unlink(missing_ok=True)

for category, value in categories.items():
    with pathlib.Path.open(
        settings,
        "a",
    ) as file:
        file.write(f"## {category}\n\n")
        file.write(typing.cast("str", value.__doc__).strip() + "\n")
