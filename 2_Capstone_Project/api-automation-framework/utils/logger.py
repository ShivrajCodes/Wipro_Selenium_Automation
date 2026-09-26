"""
Simple, consistent logger for the framework.

Using one shared logger (rather than print statements scattered
everywhere) makes debugging failed CI runs much easier, and the same
messages can be attached to Allure reports.
"""

import logging
import sys

_LOG_FORMAT = "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_logger(name: str = "api_framework") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:  # avoid duplicate handlers on repeated calls
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(_LOG_FORMAT, _DATE_FORMAT))
        logger.addHandler(handler)

    return logger


logger = get_logger()
