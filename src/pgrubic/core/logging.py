"""Logger."""

import logging

from pgrubic import PROGRAM_NAME

logging.basicConfig(
    format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger(PROGRAM_NAME)
