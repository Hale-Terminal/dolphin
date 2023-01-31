import logging
import sys
from typing import Text

import logging_loki

from dolphin import config


default_format = "%(asctime)s - %(module)s:%(funcName)s:%(lineno)d - [%(process)d][%(threadName)s] - %(levelname)s: %(message)s"


class SingleLevelFilter(logging.Filter):
    def __init__(self, passlevel, above=True):
        self.passlevel = passlevel
        self.above = above

    def filter(self, record):
        if self.above:
            return record.levelno >= self.passlevel
        else:
            return record.levelno <= self.passlevel


def get_configured_logger(name: Text = None, format: Text = None) -> logging.Logger:
    log = logging.getLogger(name or __name__)
    log.setLevel(config.LOG_LEVEL)

    formatter = logging.Formatter(format or default_format)

    general_handler = logging.StreamHandler(sys.stdout)
    general_filter = SingleLevelFilter(logging.INFO, False)
    general_handler.setFormatter(formatter)
    general_handler.addFilter(general_filter)
    log.addHandler(general_handler)

    error_handler = logging.StreamHandler(sys.stderr)
    error_filter = SingleLevelFilter(logging.WARNING)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(error_filter)
    log.addHandler(error_handler)
    log.propagate = False
    return log


log = get_configured_logger(__name__)
