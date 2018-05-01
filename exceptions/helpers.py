import traceback
import logging
import cgi

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def log_last_exception():
    logger.error(traceback.format_exc())
