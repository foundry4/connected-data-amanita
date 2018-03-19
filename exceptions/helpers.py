import traceback
import logging
import cgi

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def log_last_exception():
    logger.error(traceback.format_exc())


def format_traceback_as_html(escape=1):
    """
    returns: string

    simulates a traceback output, and, if argument escape is set to 1 (true),
    the string is converted to fit into HTML documents without problems.
    """
    import traceback, sys, string

    limit = None
    type, value, tb = sys.exc_info()
    list = traceback.format_tb(tb, limit
                               ) + traceback.format_exception_only(type, value)
    body = "Traceback (innermost last):\n" + "%-20s %s" % (
        "".join(list[:-1]), list[-1])
    if escape:
        body = '\n<PRE>' + cgi.escape(body) + '</PRE>\n'
    return body