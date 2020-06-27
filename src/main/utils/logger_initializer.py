"""
Sourced: https://aykutakin.wordpress.com/2013/08/06/logging-to-console-and-file-in-python/
"""
import logging
import os.path
from logging.handlers import RotatingFileHandler


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
    handler = RotatingFileHandler(os.path.join(output_dir, "logs/error.log"),
                                  maxBytes=10000000,
                                  backupCount=6)
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)-15s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = RotatingFileHandler(os.path.join(output_dir, "logs/debug.log"),
                                  maxBytes=10000000,
                                  backupCount=6)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)-15s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug, adding rotator
    handler = RotatingFileHandler(os.path.join(output_dir, "logs/error.log"),
                                  maxBytes=10000000,
                                  backupCount=6)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)-15s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
