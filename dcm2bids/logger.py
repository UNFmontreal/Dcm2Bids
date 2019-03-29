# -*- coding: utf-8 -*-


import logging


def setup_logging(logLevel, logFile=None):
    """ Setup logging configuration"""
    logging.basicConfig()
    logger = logging.getLogger()

    #Check level
    level = getattr(logging, logLevel.upper(), None)
    if not isinstance(level, int):
        raise ValueError("Invalid log level: {}".format(logLevel))
    logger.setLevel(level)

    #Set FileHandler
    if logFile:
        formatter = logging.Formatter(logging.BASIC_FORMAT)
        handler = logging.FileHandler(logFile)
        handler.setFormatter(formatter)
        handler.setLevel("DEBUG")
        logger.addHandler(handler)

