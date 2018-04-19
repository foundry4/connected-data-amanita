import json

import pytest

import app.api as api
from app.clients.elastic.client import ESClient
from app.clients.elastic.querybuilder.get_content import build_query_body

# response processing
from exceptions.queryexceptions import InvalidInputParameterCombination


def test_response_processing(flask_app, monkeypatch):
    # dont test parameters here just test content processing
    monkeypatch.setattr(api, 'DB_CLIENT', ESClient)  # instead of using env vars to select db
    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    raw_response_file = open("test_elastic_client/data/raw_output_100_examples.json")
    raw_response = json.load(raw_response_file)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)
    r = flask_app.get('/content')
    assert r.status_code == 200
    processed_response_file = open("test_elastic_client/data/processed_output_100_examples.json")
    processed_response = json.load(processed_response_file)
    assert json.loads(r.get_data(as_text=True)) == processed_response


# query building
def test_query_building_no_params():
    body = build_query_body()
    assert body == {'query': {'match_all': {}}, 'from': 0, 'size': 20}


def test_query_building_params_not_implemented():
    pass
    # with pytest.raises(NotImplementedError):
    #     build_query_body(published_after='')
    # with pytest.raises(NotImplementedError):
    #     build_query_body(region='')
    # with pytest.raises(NotImplementedError):
    #     build_query_body(similarity_method='')
    #     do the Nones in examples instead


def test_query_building_params_invalid_combination():
    with pytest.raises(InvalidInputParameterCombination):
        build_query_body(sort='', random=True)


def test_query_building_all_params():
    pass
