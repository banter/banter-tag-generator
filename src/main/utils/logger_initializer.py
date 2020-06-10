"""
Sourced: https://aykutakin.wordpress.com/2013/08/06/logging-to-console-and-file-in-python/
"""
import logging
import os.path
from logging.handlers import TimedRotatingFileHandler


def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)-15s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = TimedRotatingFileHandler(os.path.join(output_dir, "logs/error.log"),
                                       when="h",
                                       interval=24,
                                       backupCount=3)
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)-15s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = TimedRotatingFileHandler(os.path.join(output_dir, "logs/debug.log"),
                                       when="h",
                                       interval=6,
                                       backupCount=12)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)-15s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug, adding rotator
    handler = TimedRotatingFileHandler(os.path.join(output_dir, "logs/info.log"),
                                       when="h",
                                       interval=6,
                                       backupCount=12)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)-15s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
