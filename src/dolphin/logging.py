import logging
from dolphin.config import LOG_LEVEL


def configure_logging():
    if LOG_LEVEL == "DEBUG":
        LOGFORMAT = "%(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"
        logging.basicConfig(level=LOG_LEVEL, format=LOGFORMAT)
    else:
        logging.basicConfig(level=LOG_LEVEL)
