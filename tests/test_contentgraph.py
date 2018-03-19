import json

import pytest

from app import contentgraph
from app.clients.stardogclient import StardogClient
from app.clients import sparqlclient
from app.utils import misc
from tests.testdata import cgdata


@pytest.mark.parametrize(
    'test_data',
    [
        (cgdata.empty_graph_response, cgdata.empty_content_graph_api_response),
        (cgdata.graph_response, cgdata.content_graph_api_response)
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
    returned_content = contentgraph.get_content_from_graph({}, 'application/json')
    assert returned_content == test_data[1]


def test_get_content_from_graph_invalid_format():
    with pytest.raises(NotImplementedError):
        contentgraph.get_content_from_graph({}, 'invalidformat')
