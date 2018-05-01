import pytest

from app.apiparams import lists


class MockDefinitions:
    def __getattr__(self, item):
        return None


# test parameter lists
def test_get_param_mappers_for_endpoint_correct_content_parameter_list():
    specced_content_parameters = ['mediaType', 'sort', 'maxDuration', 'region', 'publishedAfter', 'categories', 'limit',
                                  'offset', 'random']

    implemented_content_parameters = lists.get_param_mappers_for_endpoint('content', MockDefinitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)


def test_get_param_mappers_for_endpoint_correct_similar_parameter_list():
    specced_content_parameters = ['itemUri', 'mediaType', 'sort', 'maxDuration', 'region', 'publishedAfter', 'limit',
                                  'offset', 'similarityMethod']

    implemented_content_parameters = lists.get_param_mappers_for_endpoint('similar', MockDefinitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)


def test_get_param_mappers_for_endpoint_correct_item_parameter_list():
    specced_content_parameters = ['itemUri']

    implemented_content_parameters = lists.get_param_mappers_for_endpoint('item', MockDefinitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)


def test_get_param_mappers_for_endpoint_invalid_endpoint():
    with pytest.raises(ValueError):
        lists.get_param_mappers_for_endpoint('invalid', MockDefinitions())

