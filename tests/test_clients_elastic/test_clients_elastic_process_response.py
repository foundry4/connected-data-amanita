"""Test response is processed correctly. This could """
import json

import pytest

from app.clients.elastic.process_response import map_hits_to_api_spec


@pytest.mark.parametrize('dumps', [
    ("test_clients_elastic/data/raw_output_100_examples.json",
     "test_clients_elastic/data/processed_output_100_examples.json"),
    ("test_clients_elastic/data/raw_output_100_similar_examples.json",
     "test_clients_elastic/data/processed_output_100_similar_examples.json"),
    ("test_clients_elastic/data/raw_output_item_example.json",
     "test_clients_elastic/data/processed_output_item_example.json")
])
def test_content_endpoint_map_hits_to_api_response(dumps):
    raw_response_file = open(dumps[0])
    raw_response = json.load(raw_response_file)
    mapped_response_file = open(dumps[1])
    mapped_response = json.load(mapped_response_file)
    assert map_hits_to_api_spec(raw_response) == mapped_response

