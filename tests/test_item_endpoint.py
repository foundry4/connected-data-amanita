import json

import pytest
from rdflib import URIRef

from app import contentgraph
from app.clients import sparqlclient
from app.clients.stardogclient import StardogClient
from exceptions.clientexceptions import NoResultsFoundError
from tests.testdata import cgdata
from tests.testdata.cgdata import multi_item_api_response

example_endpoint_call = '/content/http://exampleuri.com/example'


def test_item_endpoint_status(monkeypatch, flask_app):
    """Requests to /item/ should return 200"""
    monkeypatch.setattr(contentgraph, 'get_item_from_graph', lambda _: 'Some Response')
    r = flask_app.get(example_endpoint_call)
    json.loads(r.get_data(as_text=True))
    assert r.status_code == 200


def test_uri_parameter(flask_app, monkeypatch):
    # noinspection PyMethodMayBeStatic
    class FakeStardog:
        def __init__(self, *_):
            pass

        def get_item(self, _):
            return multi_item_api_response

        def initialise_namespaces(self):
            pass

    monkeypatch.setattr(contentgraph, 'StardogClient', FakeStardog)
    r = flask_app.get(example_endpoint_call)
    assert r.status_code == 200


def test_bad_stardog_endpoint_url(flask_app, monkeypatch):
    monkeypatch.setattr(contentgraph, 'STARDOG_ENDPOINT', 'http://fake_endpoint/')
    r = flask_app.get(example_endpoint_call)
    assert r.status_code == 500


def test_api_exception(flask_app, monkeypatch):
    monkeypatch.setattr(contentgraph, 'get_item_from_graph', lambda: Exception())
    r = flask_app.get(example_endpoint_call)
    assert r.status_code == 500


def test_get_item_from_graph(monkeypatch):
    """Test that get_all_content returns content from the graph store instance and formats it correctly"""

    # noinspection PyMethodMayBeStatic
    class mock_result:
        def serialize(*_, **__):
            return json.dumps(cgdata.single_item_graph_response)

    # noinspection PyMissingConstructor
    class FakeStardog(StardogClient):
        def __init__(self, *_):
            pass

        def query(*_, **__):
            return mock_result

        def initialise_namespaces(*_):
            pass

    monkeypatch.setattr(sparqlclient, 'is_result_set_empty', lambda _: False)
    monkeypatch.setattr(contentgraph, 'StardogClient', FakeStardog)
    ex_uri = URIRef('http://exampleuri.com/example')
    monkeypatch.setitem(cgdata.single_item_api_response, 'Programme', str(ex_uri))
    returned_content = contentgraph.get_item_from_graph(ex_uri)
    assert returned_content == cgdata.single_item_api_response


def test_get_item_none_found(monkeypatch):
    # noinspection PyMissingConstructor
    class FakeStardog(StardogClient):
        def __init__(self, *_):
            pass

        def query(*_, **__):
            return cgdata.empty_graph_response

        def initialise_namespaces(*_):
            pass

    monkeypatch.setattr(sparqlclient, 'is_result_set_empty', lambda _: True)
    monkeypatch.setattr(contentgraph, 'StardogClient', FakeStardog)
    ex_uri = URIRef('http://exampleuri.com/example')
    with pytest.raises(NoResultsFoundError):
        contentgraph.get_item_from_graph(ex_uri)


def test_item_endpoint_404(monkeypatch, flask_app):
    # noinspection PyMissingConstructor
    class FakeStardog(StardogClient):
        def __init__(self, *_):
            pass

        def query(*_, **__):
            return cgdata.empty_graph_response

        def initialise_namespaces(*_):
            pass

    monkeypatch.setattr(sparqlclient, 'is_result_set_empty', lambda _: True)
    monkeypatch.setattr(contentgraph, 'StardogClient', FakeStardog)
    r = flask_app.get(example_endpoint_call)
    assert r.status_code == 404
