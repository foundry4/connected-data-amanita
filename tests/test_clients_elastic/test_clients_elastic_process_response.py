"""Test response is processed correctly. This could """
import json

import pytest

import inspect

import app.api as api
from app.clients.elastic.client import ESClient

item_uri = 'programmes:bbc.co.uk,2018/FIXME/p05q11tt'

def test_content_endpoint_map_hits_to_api_response(flask_app, monkeypatch):
    # dont test parameters here just test content processing
    monkeypatch.setattr(api, 'DB_CLIENT', ESClient)  # instead of using env vars to select db
    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    raw_response_file = open("test_clients_elastic/data/raw_output_100_examples.json")
    raw_response = json.load(raw_response_file)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)
    r = flask_app.get('/content')
    assert r.status_code == 200
    processed_response_file = open("test_clients_elastic/data/processed_output_100_examples.json")
    processed_response = json.load(processed_response_file)
    assert json.loads(r.get_data(as_text=True)) == processed_response


def test_similar_endpoint_map_hits_to_api_response(flask_app, monkeypatch):
    # dont test parameters here just test content processing
    monkeypatch.setattr(api, 'DB_CLIENT', ESClient)  # instead of using env vars to select db
    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    raw_response_file = open("test_clients_elastic/data/raw_output_100_similar_examples.json")
    raw_response = json.load(raw_response_file)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)
    r = flask_app.get(f'/content/{item_uri}/similar')
    assert r.status_code == 200
    processed_response_file = open("test_clients_elastic/data/processed_output_100_similar_examples.json")
    processed_response = json.load(processed_response_file)
    assert json.loads(r.get_data(as_text=True)) == processed_response


def test_item_endpoint_map_hits_to_api_response(flask_app, monkeypatch):
    # dont test parameters here just test content processing
    monkeypatch.setattr(api, 'DB_CLIENT', ESClient)  # instead of using env vars to select db
    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    raw_response_file = open("test_clients_elastic/data/raw_output_item_example.json")
    raw_response = json.load(raw_response_file)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)
    # doesnt actually resolve but this is the endpoint used to get data dump
    r = flask_app.get('/content/programmes:bbc.co.uk,2018/FIXME/p05q11tt')
    assert r.status_code == 200
    processed_response_file = open("test_clients_elastic/data/processed_output_item_example.json")
    processed_response = json.load(processed_response_file)
    assert json.loads(r.get_data(as_text=True)) == processed_response
