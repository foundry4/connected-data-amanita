from flask import logging  # use flask logger for colours and better integration

from app.utils import global_vars


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(global_vars.LOG_LEVEL)
    return logger
