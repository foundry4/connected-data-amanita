"""API is run from here, access at localhost:5000. To run queries from browser, visit the `localhost:5000/content`
endpoint and add parameters like so `/content?limit=5`."""
import os
from urllib.request import url2pathname

from SPARQLWrapper.SPARQLExceptions import QueryBadFormed
from flask import Flask, jsonify, request, g

from app.apiparams.mapping import map_param_values_to_given_definitions
from app.clients.elastic.client import ESClient
from app.clients.sparql.client import SPARQLClient
from app.utils import constants
from app.utils import logging
from exceptions.clientexceptions import NoResultsFoundError, InvalidClientName
from exceptions.helpers import log_last_exception
from exceptions.queryexceptions import InvalidInputQuery

logger = logging.get_logger(__name__)

PORT = int(os.getenv("PORT", constants.DEFAULT_HTTP_PORT))
DB_ENDPOINT = os.getenv('DB_ENDPOINT', constants.DEFAULT_DB_ENDPOINT)
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_CLIENT = os.getenv('DB_CLIENT', constants.DEFAULT_DB_CLIENT)
logger.info(f'Using credentials:\n endpoint: {DB_ENDPOINT}\n user: {DB_USER}\n pass: {DB_PASS}')

db_client_classes = {
    'stardog': SPARQLClient,
    'elasticsearch': ESClient
}

app = Flask(__name__)


def get_client(db_client_name):
    if not hasattr(g, 'client'):
        try:
            client = db_client_classes[db_client_name](DB_ENDPOINT, DB_USER, DB_PASS)
        except KeyError:
            raise InvalidClientName(f'Client {db_client_name} is not implemented, choose from {list(db_client_classes)}')

        g.client = client
    return g.client


@app.teardown_appcontext
def close_client_connection(error=''):
    if hasattr(g, 'client'):
        g.client.close_connection()


@app.route('/', methods=['GET'])
def index():
    res = {}
    return jsonify(res)


@app.route('/content', methods=['GET'])
def list_content():
    """
    List content from content graph with optional query parameters.

    Returns:
        res (string): results encoded in json
        200 (int): success status code
    """
    query_params = request.args

    client = get_client(DB_CLIENT)
    mapped_params = map_param_values_to_given_definitions(
        client.parameter_definitions,
        'content',
        query_params=query_params
    )
    res = {"results": client.get_content(mapped_params)}
    return jsonify(res), 200


@app.route('/content/<path:item_uri>', methods=['GET'])
def item(item_uri):
    """
    List details for a single item.

    Returns:
        res (string): results encoded in json
        200 (int): success status code
    """
    client = get_client(DB_CLIENT)
    path_params = {'itemUri': url2pathname(item_uri)}
    mapped_params = map_param_values_to_given_definitions(
        client.parameter_definitions,
        'item',
        path_params=path_params
    )
    res = client.get_item(mapped_params)
    return jsonify(res), 200


@app.route('/content/<path:item_uri>/similar', methods=['GET'])
def list_similar_content(item_uri):
    """
    Return list of `similar` items, given a programme URI.

    Returns:
        res (string): results encoded in json
        200 (int): success status code
    """
    query_params = request.args

    client = get_client(DB_CLIENT)
    path_params = {'itemUri': url2pathname(item_uri)}
    mapped_params = map_param_values_to_given_definitions(
        client.parameter_definitions,
        'similar',
        query_params=query_params,
        path_params=path_params
    )

    res = {"results": client.get_similar(mapped_params)}
    return jsonify(res), 200


@app.errorhandler(Exception)
def server_error(e):
    """
    Runs when an exception is raised. Logs to console and prints HTML formatted error to browser.

    Args:
        e (Exception): python exception

    Returns:
        err (string)
        err_code (int)
    """
    log_last_exception()

    if type(e) in (InvalidInputQuery, QueryBadFormed):
        code = 400
    elif isinstance(e, NoResultsFoundError):
        code = 404
    else:
        code = 500
    e_str = str(e).replace("\n", "<br />")
    return f'<h1>Error {code}</h1>{e_str}', code


if __name__ == '__main__':  # pragma: no cover
    app.run(host='0.0.0.0', port=PORT, debug=True)
