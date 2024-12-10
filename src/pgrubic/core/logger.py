"""Logger."""

import logging

from pgrubic import PACKAGE_NAME

logging.basicConfig(
    format="[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

logger = logging.getLogger(PACKAGE_NAME)
