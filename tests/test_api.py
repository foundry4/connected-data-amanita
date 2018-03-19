"""Pytest suite to test app.contentgraph"""

import json

import pytest

from app import contentgraph
from tests.testdata.cgdata import content_graph_api_response


def test_api_root_status(flask_app):
    """Requests to the root should return 200"""
    r = flask_app.get('/')
    assert r.status_code == 200


def test_content_endpoint_status(monkeypatch, flask_app):
    """Requests to /content should return 200"""
    monkeypatch.setattr(contentgraph, 'get_content_from_graph', lambda query_params, mime_type: 'Some Response')
    r = flask_app.get('/content')
    json.loads(r.get_data(as_text=True))
    assert r.status_code == 200


def test_fake_endpoint(flask_app):
    """Requests to an invalid endpoint should 404"""
    r = flask_app.get('/fake_endpoint')
    assert r.status_code == 404


# noinspection PyMethodMayBeStatic
class FakeStardog:
    def __init__(self, *_):
        pass

    def get_content(self, _):
        return content_graph_api_response

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
    assert r.status_code == 502


def test_api_exception(flask_app, monkeypatch):
    monkeypatch.setattr(contentgraph, 'get_content_from_graph', lambda: Exception())
    r = flask_app.get(f'/content')
    assert r.status_code == 500
