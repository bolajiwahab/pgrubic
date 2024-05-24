"""Logger."""

import logging

logging.basicConfig(
    format="%(message)s",
    level=logging.ERROR,
)

logger = logging.getLogger("pgshield")
