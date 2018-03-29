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


def get_content_from_graph(validated_query_params):
    """Retrieve content from the content graph, given a set of filter parameters"""
    db_client = _init_db_client()
    results = db_client.get_content(validated_query_params)
    return map_content_to_api_spec(results)


def get_item_from_graph(validated_uri):
    """Get a single item from the content graph, given a programme URI."""
    db_client = _init_db_client()
    result = db_client.get_item(validated_uri)
    return result


def get_similar_items_from_graph(item_uri, validated_query_params):
    """Get similar items from the content graph."""
    db_client = _init_db_client()
    result = db_client.get_similar(item_uri, validated_query_params)
    return map_content_to_api_spec(result)


def _init_db_client():
    db_client = StardogClient(STARDOG_ENDPOINT, STARDOG_USER, STARDOG_PASS)
    db_client.initialise_namespaces()
    return db_client
