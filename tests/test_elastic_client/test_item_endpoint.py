import json

import pytest

import inspect

import app.api as api
from app.clients.elastic.client import ESClient
from app.clients.elastic.querybuilder.get_item import build_query_body

# response processing
from exceptions.queryexceptions import InvalidInputParameterCombination


def test_response_processing(flask_app, monkeypatch):
    # dont test parameters here just test content processing
    monkeypatch.setattr(api, 'DB_CLIENT', ESClient)  # instead of using env vars to select db
    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    raw_response_file = open("test_elastic_client/data/raw_output_item_example.json")
    raw_response = json.load(raw_response_file)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)
    # doesnt actually resolve but this is the endpoint used to get data dump
    r = flask_app.get('/content/programmes:bbc.co.uk,2018/FIXME/p05q11tt')
    assert r.status_code == 200
    processed_response_file = open("test_elastic_client/data/processed_output_item_example.json")
    processed_response = json.load(processed_response_file)
    assert json.loads(r.get_data(as_text=True)) == processed_response


# query building
def test_query_building_no_params():
    body = build_query_body('item_uri')
    assert body == {'query': {'term': {'_id': 'item_uri'}}}
