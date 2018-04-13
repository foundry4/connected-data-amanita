"""API is run from here, access at localhost:5000. To run queries from browser, visit the `localhost:5000/content`
endpoint and add parameters like so `/content?limit=5`."""
import logging
from urllib.request import url2pathname

from SPARQLWrapper.SPARQLExceptions import QueryBadFormed
from flask import Flask, jsonify, request, g
import os

from app.clients.elasticsearch import ESClient
from app.clients.sparql import SPARQLClient
from app.utils import constants
from exceptions.clientexceptions import NoResultsFoundError
from exceptions.helpers import log_last_exception, format_traceback_as_html
from exceptions.queryexceptions import InvalidInputQuery
from app.utils.processquery import process_list_content_query_params, process_item_query_uri, \
    process_list_similar_query_params

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
db_clients = {
    'stardog': SPARQLClient,
    'elasticsearch': ESClient
}

PORT = int(os.getenv("PORT", constants.DEFAULT_HTTP_PORT))
DB_ENDPOINT = os.getenv('DB_ENDPOINT', constants.DEFAULT_DB_ENDPOINT)
DB_USER = os.getenv('DB_USER', constants.DEFAULT_DB_USER)
DB_PASS = os.getenv('DB_PASS', constants.DEFAULT_DB_PASS)
DB_CLIENT = db_clients[os.getenv('DB_CLIENT', constants.DEFAULT_DB_CLIENT)]
logger.info(f'Using credentials:\n endpoint: {DB_ENDPOINT}\n user: {DB_USER}\n pass: {DB_PASS}')

app = Flask(__name__)


def get_db():
    if not hasattr(g, 'database'):
        sd = DB_CLIENT(DB_ENDPOINT, DB_USER, DB_PASS)
        g.database = sd
    return g.database


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'database'):
        g.database.close_connection()


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
    validated_query_params = process_list_content_query_params(query_params)
    db = get_db()
    res = db.get_content(validated_query_params)
    return jsonify(res), 200


@app.route('/content/<path:item_uri>', methods=['GET'])
def item(item_uri):
    """
    List details for a single item.

    Returns:
        res (string): results encoded in json
        200 (int): success status code
    """
    validated_uri = process_item_query_uri(item_uri)
    db = get_db()
    res = db.get_item(validated_uri)
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
    validated_query_params = process_list_similar_query_params(query_params)
    validated_uri = process_item_query_uri(url2pathname(item_uri))
    db = get_db()
    res = db.get_similar(validated_uri, validated_query_params)
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
    html_traceback = format_traceback_as_html()
    if type(e) in (InvalidInputQuery, QueryBadFormed):
        return html_traceback, 400
    if isinstance(e, NoResultsFoundError):
        return html_traceback, 404
    else:
        return html_traceback, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
