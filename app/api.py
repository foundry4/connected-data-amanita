"""API is run from here, access at localhost:5000. To run queries from browser, visit the `localhost:5000/content`
endpoint and add parameters like so `/content?limit=5`."""

from SPARQLWrapper.SPARQLExceptions import QueryBadFormed
from flask import Flask, jsonify, request, logging

from app import contentgraph
from exceptions.clientexceptions import DBClientResponseError
from exceptions.helpers import log_last_exception, format_traceback_as_html
from exceptions.queryexceptions import InvalidInputQuery
from app.utils.processquery import process_query_params

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    res = {}
    return jsonify(res)


@app.route('/content', methods=['GET'])
def list_content():
    """
    List content from content graph with optional query parameters.

    Returns:
        err (string)
        err_code (int)
    """
    query_params = request.args
    validated_query_params = process_query_params(query_params)
    res = contentgraph.get_content_from_graph(validated_query_params, mime_type='application/json')
    return jsonify(res), 200


@app.errorhandler(Exception)
def server_error(e):
    """
    Runs when an exception is raised.

    Args:
        e (Exception): python exception

    Returns:
        err (string)
        err_code (int)
    """
    log_last_exception()
    if isinstance(e, DBClientResponseError):
        return format_traceback_as_html(), 502
    if type(e) in (InvalidInputQuery, QueryBadFormed):
        return format_traceback_as_html(), 400
    else:
        return format_traceback_as_html(), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
