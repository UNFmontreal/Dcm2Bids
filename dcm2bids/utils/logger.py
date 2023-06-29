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
    sh_fmt = logging.Formatter(fmt="%(levelname)-8s| %(message)s")
    sh.setFormatter(sh_fmt)

    # default formatting is kept for the log file"
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s.%(msecs)02d - %(levelname)-8s - %(module)s.%(funcName)s | "
        "%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[fh, sh]
    )
