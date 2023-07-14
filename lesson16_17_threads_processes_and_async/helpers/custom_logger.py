import logging
import sys


class ColoredFormatter(logging.Formatter):

    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    BROWN = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    GREY = '\033[0;37m'

    DARK_GREY = '\033[1;30m'
    LIGHT_RED = '\033[1;31m'
    LIGHT_GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    LIGHT_BLUE = '\033[1;34m'
    LIGHT_PURPLE = '\033[1;35m'
    LIGHT_CYAN = '\033[1;36m'
    WHITE = '\033[1;37m'

    RESET = "\033[0m"

    format = "%(asctime)s.%(msecs)03d %(levelname)s [%(processName)s: %(threadName)s] -> %(message)s"
    datefmt = "%Y-%m-%d,%H:%M:%S"

    FORMATS = {
        logging.INFO: GREEN + format + RESET,
        logging.DEBUG: BLUE + format + RESET,
        logging.WARNING: YELLOW + format + RESET,
        logging.ERROR: LIGHT_RED + format + RESET,
        logging.CRITICAL: RED + format + RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setup_logging(logger_name: str):
    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d %(levelname)s "
               "[%(name)s:%(funcName)s] [%(processName)s: %(threadName)s] -> %(message)s",
        datefmt="%Y-%m-%d,%H:%M:%S",
        stream=sys.stdout,
        level=logging.DEBUG
    )
    logger = logging.getLogger(logger_name)
    logger.propagate = False

    ch = logging.StreamHandler()
    ch.setFormatter(ColoredFormatter())
    logger.addHandler(ch)

    return logger
