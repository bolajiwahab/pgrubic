"""Logger."""

import logging

from rich.logging import RichHandler

from pgrubic import PACKAGE_NAME

logging.basicConfig(
    datefmt="%Y-%m-%dT%H:%M:%S",
    format="%(message)s",
    handlers=[RichHandler(show_path=False)],
)

logger = logging.getLogger(PACKAGE_NAME)
