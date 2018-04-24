"""Test APIs surface level to make sure correct responses are being served in different cases. Mock all client stuff."""
import pytest
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed

import app.api as api
from exceptions.clientexceptions import NoResultsFoundError, InvalidClientName
from exceptions.queryexceptions import InvalidInputQuery


class MockDefinitions:
    def __getattr__(self, item):
        return None


class MockDBClient:
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

    @property
    def parameter_definitions(self):
        return MockDefinitions()


class FakeContext:
    pass


def test_get_client_and_close(monkeypatch):
    # coverage doesnt seem to register for this test
    monkeypatch.setattr(api, 'g', FakeContext())
    monkeypatch.setattr(api, 'db_client_classes', {'mock_db_client': MockDBClient})
    assert not hasattr(api.g, 'client')

    client = api.get_client('mock_db_client')
    assert isinstance(client, MockDBClient)
    assert hasattr(api.g, 'client')

    api.close_client_connection()
    assert api.g.client.close_connection_called


def test_get_invalid_client(monkeypatch):
    monkeypatch.setattr(api, 'g', FakeContext())
    with pytest.raises(InvalidClientName):
        api.get_client('invalid_client')


def test_api_root_status(flask_app):
    """Requests to the root should return 200"""
    r = flask_app.get('/')
    assert r.status_code == 200


def test_api_content_endpoint(flask_app, monkeypatch):
    monkeypatch.setattr(api, 'db_client_classes', {'mock_db_client': MockDBClient})
    monkeypatch.setattr(api, 'DB_CLIENT', 'mock_db_client')
    monkeypatch.setattr(api, 'map_content_query_params_to_db_compatible', lambda *_: {})
    r = flask_app.get('/content')
    assert r.status_code == 200


def test_api_item_endpoint(flask_app, monkeypatch):
    monkeypatch.setattr(api, 'db_client_classes', {'mock_db_client': MockDBClient})
    monkeypatch.setattr(api, 'DB_CLIENT', 'mock_db_client')
    monkeypatch.setattr(api, 'map_item_query_uri_to_db_compatible', lambda *_: {})
    r = flask_app.get('/content/randomitempid')
    assert r.status_code == 200


def test_api_similar_endpoint(flask_app, monkeypatch):
    monkeypatch.setattr(api, 'db_client_classes', {'mock_db_client': MockDBClient})
    monkeypatch.setattr(api, 'DB_CLIENT', 'mock_db_client')
    monkeypatch.setattr(api, 'map_similar_query_params_to_db_compatible', lambda *_: {})
    monkeypatch.setattr(api, 'map_item_query_uri_to_db_compatible', lambda *_: {})
    r = flask_app.get('/content/randomitempid/similar')
    assert r.status_code == 200


@pytest.mark.parametrize(
    'endpoint', ['/content', '/content/randomitempid', '/content/randomitempid/similar']
)
@pytest.mark.parametrize(
    'query_exception', [InvalidInputQuery, QueryBadFormed]
)
def test_invalid_input_query_caught(flask_app, monkeypatch, endpoint, query_exception):
    class QueryExceptionMockDB(MockDBClient):
        def get_content(self, *_):
            raise query_exception()

        def get_similar(self, *_):
            raise query_exception()

        def get_item(self, *_):
            raise query_exception()

    monkeypatch.setattr(api, 'db_client_classes', {'mock_db_client': QueryExceptionMockDB})
    monkeypatch.setattr(api, 'DB_CLIENT', 'mock_db_client')
    monkeypatch.setattr(api, 'map_similar_query_params_to_db_compatible', lambda *_: {})
    monkeypatch.setattr(api, 'map_content_query_params_to_db_compatible', lambda *_: {})
    monkeypatch.setattr(api, 'map_item_query_uri_to_db_compatible', lambda *_: {})
    r = flask_app.get(endpoint)
    assert r.status_code == 400


def test_no_results(flask_app, monkeypatch):
    class QueryExceptionMockDB(MockDBClient):
        def get_item(self, *_):
            raise NoResultsFoundError()

    monkeypatch.setattr(api, 'db_client_classes', {'mock_db_client': QueryExceptionMockDB})
    monkeypatch.setattr(api, 'DB_CLIENT', 'mock_db_client')
    monkeypatch.setattr(api, 'map_item_query_uri_to_db_compatible', lambda *_: {})
    r = flask_app.get('/content/randomitempid')
    assert r.status_code == 404


@pytest.mark.parametrize(
    'endpoint', ['/content', '/content/randomitempid', '/content/randomitempid/similar']
)
def test_server_error_exception(flask_app, monkeypatch, endpoint):
    class ExceptionMockDB(MockDBClient):
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
