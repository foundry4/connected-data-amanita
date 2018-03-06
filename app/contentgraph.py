import os

from flask import logging

from app.clients.stardogclient import StardogClient
from app.utils import constants
from app.utils.conversions import map_content_to_api_spec

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

STARDOG_ENDPOINT = os.getenv('STARDOG_ENDPOINT', constants.DEFAULT_STARDOG_ENDPOINT)
STARDOG_USER = os.getenv('STARDOG_USER', constants.DEFAULT_STARDOG_USER)
STARDOG_PASS = os.getenv('STARDOG_PASS', constants.DEFAULT_STARDOG_PASS)
logger.info(f'Using credentials:\n endpoint: {STARDOG_ENDPOINT}\n user: {STARDOG_USER}\n pass: {STARDOG_PASS}')


def get_content_from_graph(validated_query_params, mime_type):
    """Retrieve relevant content from the content graph, given a set of filter parameters"""
    db_client = StardogClient(STARDOG_ENDPOINT, STARDOG_USER, STARDOG_PASS)
    if mime_type != 'application/json':
        raise NotImplementedError("Format '%s' not implemented." % mime_type)
    db_client.initialise_namespaces()
    results = db_client.get_content(validated_query_params)
    return map_content_to_api_spec(results)
