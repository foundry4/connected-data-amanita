import inspect
import json

import pytest

from app.clients.elastic.querybuilder.get_similar import build_query_body

item_uri = 'programmes:bbc.co.uk,2018/FIXME/p05q11tt'


# query building
def test_query_building_no_params():
    body = build_query_body(item_uri=item_uri)
    expected = {
        'query': {
            'bool': {
                'should': [{
                    'more_like_this': {
                        'like': {
                            '_index': 'pips',
                            '_type': 'clip',
                            '_id': item_uri
                        },
                        'fields': ['title', 'masterBrand.mid', 'mediaType'],
                        'min_term_freq': 1,
                        'min_doc_freq': 1
                    }
                }, {
                    'nested': {
                        'path': 'genres',
                        'query': {
                            'more_like_this': {
                                'fields': ['genres.key'],
                                'like': {
                                    '_index': 'pips',
                                    '_type': 'clip',
                                    '_id': item_uri
                                },
                                'min_term_freq': 1,
                                'min_doc_freq': 1
                            }
                        }
                    }
                }]
            }
        },
        'from': 0,
        'size': 20
    }
    assert body == expected


non_implemented_params = ['published_after', 'region', 'similarity_method']


@pytest.mark.parametrize('non_implemented_param', non_implemented_params)
def test_query_building_params_not_implemented(non_implemented_param):
    with pytest.raises(NotImplementedError):
        build_query_body(**{non_implemented_param: ''})


def test_query_building_all_implemented_params():
    params = json.load(open("test_clients_elastic/data/param_examples.json"))
    expected_params = list(inspect.signature(build_query_body).parameters)

    val_params = {k: v['validated'] for k, v in params.items() if
                  k not in non_implemented_params and k in expected_params}
    body = build_query_body(**val_params)
    expected = {
        'query': {
            'bool': {
                'filter': [{
                    'term': {
                        'mediaType': 'audio'
                    }
                }, {
                    'term': {
                        'mediaType': 'video'
                    }
                },
                    {
                        'range': {
                            'duration': {
                                'lte': 100
                            }
                        }
                    }
                ],
                'should': [{
                    'more_like_this': {
                        'like': {
                            '_index': 'pips',
                            '_type': 'clip',
                            '_id': 'http://exampleuri.com'
                        },
                        'fields': [
                            'title',
                            'masterBrand.mid',
                            'mediaType'
                        ],
                        'min_term_freq': 1,
                        'min_doc_freq': 1
                    }
                },
                    {
                        'nested': {
                            'path': 'genres',
                            'query': {
                                'more_like_this': {
                                    'fields': [
                                        'genres.key'
                                    ],
                                    'like': {
                                        '_index': 'pips',
                                        '_type': 'clip',
                                        '_id': 'http://exampleuri.com'
                                    },
                                    'min_term_freq': 1,
                                    'min_doc_freq': 1
                                }
                            }
                        }
                    }
                ],
                'minimum_should_match': 1
            }
        },
        'from': 10,
        'size': 10
    }
    assert body == expected
