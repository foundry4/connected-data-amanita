from flask import logging  # use flask logger for colours and better integration

from app.utils import constants


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(constants.LOG_LEVEL)
    return logger
