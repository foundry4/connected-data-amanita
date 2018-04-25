import json

import pytest

from app.clients.elastic.client import ESClient


# dont test parameters here just test content processing
from exceptions.clientexceptions import NoResultsFoundError


def test_get_content(monkeypatch):
    raw_response_file = open("tests/test_clients_elastic/data/raw_output_2_examples.json")
    raw_response = json.load(raw_response_file)

    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)

    client = ESClient('', '', '')
    mapped_response = client.get_content({})

    expected_response_file = open("tests/test_clients_elastic/data/processed_output_2_examples.json")
    expected_response = {
        'results': json.load(expected_response_file)
    }
    assert mapped_response == expected_response


def test_get_content_no_results(monkeypatch):
    raw_response_file = open("tests/test_clients_elastic/data/no_hits.json")
    raw_response = json.load(raw_response_file)

    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)

    client = ESClient('', '', '')
    mapped_response = client.get_content({})

    expected_response = {
        'results': []
    }
    assert mapped_response == expected_response


def test_get_similar(monkeypatch):
    raw_response_file = open("tests/test_clients_elastic/data/raw_output_2_similar_examples.json")
    raw_response = json.load(raw_response_file)

    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)

    client = ESClient('', '', '')
    mapped_response = client.get_similar({'item_uri': None})

    expected_response_file = open("tests/test_clients_elastic/data/processed_output_2_similar_examples.json")
    expected_response = {
        'results': json.load(expected_response_file)
    }
    assert mapped_response == expected_response


def test_get_similar_no_results(monkeypatch):
    raw_response_file = open("tests/test_clients_elastic/data/no_hits.json")
    raw_response = json.load(raw_response_file)

    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)

    client = ESClient('', '', '')
    mapped_response = client.get_similar({'item_uri': None})

    expected_response = {
        'results': []
    }
    assert mapped_response == expected_response


def test_get_item(monkeypatch):
    raw_response_file = open("tests/test_clients_elastic/data/raw_output_item_example.json")
    raw_response = json.load(raw_response_file)

    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)

    client = ESClient('', '', '')
    mapped_response = client.get_item({'item_uri': None})

    expected_response_file = open("tests/test_clients_elastic/data/processed_output_item_example.json")
    expected_response = json.load(expected_response_file)[0]
    assert mapped_response == expected_response


def test_get_item_no_results(monkeypatch):
    raw_response_file = open("tests/test_clients_elastic/data/no_hits.json")
    raw_response = json.load(raw_response_file)

    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: raw_response)

    client = ESClient('', '', '')
    with pytest.raises(NoResultsFoundError):
        client.get_item({'item_uri': None})
