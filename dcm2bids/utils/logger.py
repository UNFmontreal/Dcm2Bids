# -*- coding: utf-8 -*-

"""Setup logging configuration"""

import logging
import sys


def setup_logging(log_level, log_file=None):
    """ Setup logging configuration"""
    # Check level
    level = getattr(logging, log_level.upper(), None)
    if not isinstance(level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    fh = logging.FileHandler(log_file)
    # fh.setFormatter(formatter)
    fh.setLevel("DEBUG")

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(log_level)
    sh_fmt = CustomFormatter(fmt="%(levelname)-8s| %(message)s")
    sh.setFormatter(sh_fmt)

    # default formatting is kept for the log file"
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)02d - %(levelname)-8s - %(module)s.%(funcName)s | "
        "%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[fh, sh]
    )


class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)