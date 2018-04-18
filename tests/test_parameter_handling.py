from app.apiparams import lists, types, validator


class Definitions:
    def __getattr__(self, item):
        return None

# test parameter lists
def test_correct_content_parameter_list():
    specced_content_parameters = ['mediaType', 'sort', 'maxDuration', 'region', 'publishedAfter', 'categories', 'limit',
                                  'offset', 'random']

    implemented_content_parameters = lists.get_param_validators_for_endpoint('content', Definitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)


def test_correct_similar_parameter_list():
    specced_content_parameters = ['mediaType', 'sort', 'maxDuration', 'region', 'publishedAfter', 'limit',
                                  'offset', 'similarityMethod']

    implemented_content_parameters = lists.get_param_validators_for_endpoint('similar', Definitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)


def test_correct_item_parameter_list():
    specced_content_parameters = ['item_uri']

    implemented_content_parameters = lists.get_param_validators_for_endpoint('item', Definitions())
    assert sorted(implemented_content_parameters) == sorted(specced_content_parameters)

# test parameter types
#TODO : HERE