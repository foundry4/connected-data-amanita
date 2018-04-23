import json

import pytest

import inspect

from rdflib import URIRef

import app.api as api
from app.clients.elastic.client import ESClient
from app.clients.elastic.querybuilder.get_item import build_query_body

# response processing
from exceptions.clientexceptions import NoResultsFoundError



# query building
def test_query_building_no_params():
    body = build_query_body('item_uri')
    assert body == {'query': {'term': {'_id': 'item_uri'}}}


def test_no_item_found(monkeypatch, flask_app):
    monkeypatch.setattr(api, 'DB_CLIENT', ESClient)  # instead of using env vars to select db
    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_, **__: None)
    no_hits_file = open("test_clients_elastic/data/no_hits.json")
    no_hits = json.load(no_hits_file)
    monkeypatch.setattr(ESClient, 'query', lambda *_, **__: no_hits)
    monkeypatch.setattr(ESClient, 'setup_connection', lambda *_: None)
    client = ESClient('', '', '')
    with pytest.raises(NoResultsFoundError):
        client.get_item(URIRef('non_existant_uri'))
