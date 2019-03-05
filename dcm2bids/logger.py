# -*- coding: utf-8 -*-


import logging


def setup_logging(logLevel, logFile=None):
    """ Setup logging configuration"""
    conf = {}

    #Check level
    level = getattr(logging, logLevel.upper(), None)
    if not isinstance(level, int):
        raise ValueError("Invalid log level: {}".format(logLevel))
    conf["level"] = level

    #Set filename
    if logFile:
        conf["filename"] = logFile

    logging.basicConfig(**conf)

