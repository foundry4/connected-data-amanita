"""Pytest suite to test app.contentgraph"""

import json

import pytest

from app import contentgraph
from app.clients import sparqlclient
from tests.testdata import cgdata
from tests.testdata.cgdata import multi_item_api_response
from app.clients.stardogclient import StardogClient


def test_content_endpoint_status(monkeypatch, flask_app):
    """Requests to /content should return 200"""
    monkeypatch.setattr(contentgraph, 'get_content_from_graph', lambda _: 'Some Response')
    r = flask_app.get('/content')
    json.loads(r.get_data(as_text=True))
    assert r.status_code == 200


# noinspection PyMethodMayBeStatic
class FakeStardog:
    def __init__(self, *_):
        pass

    def get_content(self, _):
        return multi_item_api_response

    def initialise_namespaces(self):
        pass


raw_query_params = ['media=video', 'maxDuration=PT30M', 'region=uk', 'publishedAfter=2012-05-30T09:00:00',
                    'categories=genre', 'tags=tag', 'limit=10', 'offset=1', 'sort=-duration']


@pytest.mark.parametrize(
    'params', raw_query_params + ['&'.join(raw_query_params)]
)
def test_parameters(flask_app, monkeypatch, params):
    monkeypatch.setattr(contentgraph, 'StardogClient', FakeStardog)
    r = flask_app.get(f'/content?{params}')
    assert r.status_code == 200


raw_query_params_multi_val = ['media=audio', 'media=video', 'categories=genre1', 'categories=genre2', 'tags=tag1',
                              'tags=tag2']


@pytest.mark.parametrize(
    'params', raw_query_params_multi_val
)
def test_parameters_multi_val(flask_app, monkeypatch, params):
    monkeypatch.setattr(contentgraph, 'StardogClient', FakeStardog)
    r = flask_app.get(f'/content?{params}')
    assert r.status_code == 200


raw_query_params_bad_values = ['media=wrong', 'region=france']


@pytest.mark.parametrize('params', raw_query_params_bad_values)
def test_bad_param_values(flask_app, monkeypatch, params):
    monkeypatch.setattr(contentgraph, 'StardogClient', FakeStardog)
    r = flask_app.get(f'/content?{params}')
    assert r.status_code == 400


raw_query_params_bad_names = ['fakeparam1=fakeval', 'fakeparam2=fakeval2', 'fakeparam2=fakeval3']


@pytest.mark.parametrize('params', raw_query_params_bad_names)
def test_bad_param_names(flask_app, monkeypatch, params):
    monkeypatch.setattr(contentgraph, 'StardogClient', FakeStardog)
    r = flask_app.get(f'/content?{params}')
    assert r.status_code == 400


raw_query_params_too_many_vals = [['maxDuration=PT30M', 'maxDuration=PT40M'], ['region=ex-uk', 'region=uk'],
                                  ['publishedAfter=2012-05-30T09:00:00', 'publishedAfter=2013-05-30T09:00:00'],
                                  ['limit=10', 'limit=20'], ['offset=10', 'offset=20']]


@pytest.mark.parametrize('params', raw_query_params_too_many_vals)
def test_too_many_param_values(flask_app, monkeypatch, params):
    monkeypatch.setattr(contentgraph, 'StardogClient', FakeStardog)
    r = flask_app.get(f'/content?{"&".join(params)}')
    assert r.status_code == 400


def test_bad_stardog_endpoint_url(flask_app, monkeypatch):
    monkeypatch.setattr(contentgraph, 'STARDOG_ENDPOINT', 'http://fake_endpoint/')
    r = flask_app.get('/content')
    assert r.status_code == 500


def test_api_exception(flask_app, monkeypatch):
    monkeypatch.setattr(contentgraph, 'get_content_from_graph', lambda: Exception())
    r = flask_app.get(f'/content')
    assert r.status_code == 500


@pytest.mark.parametrize(
    'test_data',
    [
        (cgdata.empty_graph_response, cgdata.empty_multi_item_api_response),
        (cgdata.multi_item_graph_response, cgdata.multi_item_api_response)
    ]
)
def test_get_content_from_graph(monkeypatch, test_data):
    """Test that get_all_content returns content from the graph store instance and formats it correctly"""

    # noinspection PyMethodMayBeStatic
    class mock_result:
        def serialize(*_, **__):
            return json.dumps(test_data[0])

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
    returned_content = contentgraph.get_content_from_graph({})
    assert returned_content == test_data[1]
