"""PyTest Suite for testing utitilies for processing a response from a SPARQL endpoint"""

import pytest

from app.utils.processresponse import get_bindings_from_response, transform_bindings
from exceptions.queryexceptions import InvalidQueryResponse
from tests.testdata import cgdata as cg


def test_get_bindings_from_response():
    valid_resp = get_bindings_from_response(cg.multi_item_graph_response)
    assert valid_resp == cg.multi_item_graph_response['results']['bindings']

    assert get_bindings_from_response({'results': {'bindings': []}}) == []

    with pytest.raises(InvalidQueryResponse):
        get_bindings_from_response({})

    with pytest.raises(InvalidQueryResponse):
        get_bindings_from_response({'results': {}})

    with pytest.raises(InvalidQueryResponse):
        get_bindings_from_response({'results': {'bindings': ''}})


def test_transform_bindings():
    transformed = transform_bindings(cg.multi_item_graph_response['results']['bindings'])
    assert transformed == cg.multi_item_api_response['Results']

    assert transform_bindings([]) == []
