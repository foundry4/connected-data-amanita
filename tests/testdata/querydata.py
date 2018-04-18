from copy import copy

from rdflib import URIRef, Literal
from rdflib.namespace import XSD
from werkzeug.datastructures import MultiDict

from app.apiparams.validator import ParamValidator


# test all rdf datatypes in both single and list form

def get_single_query_parameter_test_mappings_restricted():
    single_query_parameter_test_mappings_restricted = {
        'string': ParamValidator(
            snake_case_name='string',
            param_type=Literal,
            is_list=False,
            datatype=XSD.string,
            allowed_values=['string1', 'string2', 'string3']
        ),
        'duration': ParamValidator(
            snake_case_name='duration',
            param_type=Literal,
            is_list=False,
            datatype=XSD.duration,
            allowed_values=['0.1', '0.2', '0.3']
        ),
        'datetime': ParamValidator(
            snake_case_name='datetime',
            param_type=Literal,
            is_list=False,
            datatype=XSD.datetime,
            allowed_values=['2018-01-01T00:00:00', '2018-01-02T00:00:00', '2018-01-03T00:00:00', ]
        ),
        'uri': ParamValidator(
            snake_case_name='uri',
            param_type=URIRef,
            is_list=False,
            allowed_values=['http://purl.org/bbcrd/mango/tag1', 'http://purl.org/bbcrd/mango/tag2',
                            'http://purl.org/bbcrd'
                            '/mango/tag3']
        ),
    }
    return single_query_parameter_test_mappings_restricted


def get_single_query_parameter_test_mappings():
    single_query_parameter_test_mappings = {}
    for param_name, param_obj in get_single_query_parameter_test_mappings_restricted().items():
        param_obj_non_restricted = copy(param_obj)
        param_obj_non_restricted.allowed_values = None
        single_query_parameter_test_mappings[param_name] = param_obj_non_restricted
    return single_query_parameter_test_mappings


def get_multi_query_parameter_test_mappings_restricted():
    multi_query_parameter_test_mappings_restricted = {}
    for param_name, param_obj in get_single_query_parameter_test_mappings_restricted().items():
        multi_param_obj = copy(param_obj)
        multi_param_obj.is_list = True
        multi_query_parameter_test_mappings_restricted[param_name] = multi_param_obj
    return multi_query_parameter_test_mappings_restricted


def get_multi_query_parameter_test_mappings():
    multi_query_parameter_test_mappings = {}
    for param_name, param_obj in get_single_query_parameter_test_mappings_restricted().items():
        multi_param_obj_non_restricted = copy(param_obj)
        multi_param_obj_non_restricted.is_list = True
        multi_param_obj_non_restricted.allowed_values = None
        multi_query_parameter_test_mappings[param_name] = multi_param_obj_non_restricted
    return multi_query_parameter_test_mappings


# for testing normal input query params
input_query_params_multidict_allowed = MultiDict([
    ('string', 'string1'),
    ('duration', '0.1'),
    ('datetime', '2018-01-01T00:00:00'),
    ('uri', 'http://purl.org/bbcrd/mango/tag1'),
])

input_query_params_multidict_not_allowed = MultiDict([
    ('string', 'n'),
    ('duration', 'n'),
    ('datetime', 'n'),
    ('uri', 'n'),
])

multi_input_query_params_multidict_allowed = MultiDict([
    ('string', 'string2'),
    ('string', 'string3'),
    ('duration', '0.2'),
    ('duration', '0.3'),
    ('datetime', '2018-01-02T00:00:00'),
    ('datetime', '2018-01-03T00:00:00'),
    ('uri', 'http://purl.org/bbcrd/mango/tag2'),
    ('uri', 'http://purl.org/bbcrd/mango/tag3'),
])

multi_input_query_params_multidict_some_allowed = MultiDict([
    ('string', 'string2'),
    ('string', 'n'),
    ('duration', '0.2'),
    ('duration', 'n'),
    ('datetime', '2018-01-02T00:00:00'),
    ('datetime', 'n'),
    ('uri', 'http://purl.org/bbcrd/mango/tag2'),
    ('uri', 'n'),
])

multi_input_query_params_multidict_not_allowed = MultiDict([
    ('string', 'n'),
    ('string', 'n'),
    ('duration', 'n'),
    ('duration', 'n'),
    ('datetime', 'n'),
    ('datetime', 'n'),
    ('uri', 'n'),
    ('uri', 'n'),
])

# for testing invalid inputs
invalid_input_query_params_multidict = MultiDict([
    ('invalid_single', 'a'),
    ('invalid_multi', 'b'),
    ('invalid_multi', 'c'),
])

# input query parameters and values in dict form ###


# for testing normal input query params
input_query_params_dict_allowed = {
    'string': 'string1',
    'duration': '0.1',
    'datetime': '2018-01-01T00:00:00',
    'uri': 'http://purl.org/bbcrd/mango/tag1',
}

multi_input_query_params_dict_allowed = {
    'string': ['string2', 'string3'],
    'duration': ['0.2', '0.3'],
    'datetime': ['2018-01-02T00:00:00', '2018-01-03T00:00:00'],
    'uri': ['http://purl.org/bbcrd/mango/tag2', 'http://purl.org/bbcrd/mango/tag3']
}


# for testing empty
empty_input_query_params_multidict = MultiDict()
empty_input_query_params_dict = {}
