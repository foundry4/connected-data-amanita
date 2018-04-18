"""Test APIs surface level to make sure correct responses are being served in different cases. Mock all client stuff."""
import pytest
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed

import app.api as api
from exceptions.clientexceptions import NoResultsFoundError
from exceptions.queryexceptions import InvalidInputQuery


class MockDB:
    close_connection_called = False

    def __init__(self, *_):
        pass

    def close_connection(self):
        self.close_connection_called = True

    def get_content(self, *_):
        pass

    def get_similar(self, *_):
        pass

    def get_item(self, *_):
        pass

    def process_content_query_params(self, *_):
        pass

    def process_item_query_uri(self, *_):
        pass

    def process_similar_query_params(self, *_):
        pass


def test_get_client_and_close(monkeypatch):
    monkeypatch.setattr(api, 'DB_CLIENT', MockDB)
    with api.app.app_context():
        assert not hasattr(api.g, 'client')
        client = api.get_client()
        assert isinstance(client, MockDB)
        assert hasattr(api.g, 'client')
        api.close_client_connection()
        assert api.g.client.close_connection_called


def test_api_root_status(flask_app):
    """Requests to the root should return 200"""
    r = flask_app.get('/')
    assert r.status_code == 200


def test_api_content_endpoint(flask_app, monkeypatch):
    monkeypatch.setattr(api, 'DB_CLIENT', MockDB)
    r = flask_app.get('/content')
    assert r.status_code == 200


def test_api_item_endpoint(flask_app, monkeypatch):
    monkeypatch.setattr(api, 'DB_CLIENT', MockDB)
    r = flask_app.get('/content/randomitempid')
    assert r.status_code == 200


def test_api_similar_endpoint(flask_app, monkeypatch):
    monkeypatch.setattr(api, 'DB_CLIENT', MockDB)
    r = flask_app.get('/content/randomitempid/similar')
    assert r.status_code == 200


@pytest.mark.parametrize(
    'endpoint', ['/content', '/content/randomitempid', '/content/randomitempid/similar']
)
@pytest.mark.parametrize(
    'query_exception', [InvalidInputQuery, QueryBadFormed]
)
def test_invalid_input_query_caught(flask_app, monkeypatch, endpoint, query_exception):
    class QueryExceptionMockDB(MockDB):
        def get_content(self, *_):
            raise query_exception()

        def get_similar(self, *_):
            raise query_exception()

        def get_item(self, *_):
            raise query_exception()

    monkeypatch.setattr(api, 'DB_CLIENT', QueryExceptionMockDB)
    r = flask_app.get(endpoint)
    assert r.status_code == 400


def test_no_results(flask_app, monkeypatch):
    class QueryExceptionMockDB(MockDB):
        def get_item(self, *_):
            raise NoResultsFoundError()

    monkeypatch.setattr(api, 'DB_CLIENT', QueryExceptionMockDB)
    r = flask_app.get('/content/randomitempid')
    assert r.status_code == 404


@pytest.mark.parametrize(
    'endpoint', ['/content', '/content/randomitempid', '/content/randomitempid/similar']
)
def test_server_error_exception(flask_app, monkeypatch, endpoint):
    class ExceptionMockDB(MockDB):
        def get_content(self, *_):
            raise Exception()

        def get_similar(self, *_):
            raise Exception()

        def get_item(self, *_):
            raise Exception()

    monkeypatch.setattr(api, 'DB_CLIENT', ExceptionMockDB)
    r = flask_app.get(endpoint)
    assert r.status_code == 500


def test_fake_endpoint(flask_app):
    """Requests to an invalid endpoint should 404"""
    r = flask_app.get('/fake_endpoint')
    assert r.status_code == 404
