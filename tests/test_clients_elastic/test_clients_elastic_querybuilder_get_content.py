import inspect
import json

import pytest

from app.clients.elastic.querybuilder import get_content
from app.clients.elastic.querybuilder.get_content import build_query_body
from exceptions.queryexceptions import InvalidInputParameterCombination


# query building
def test_build_query_body_no_params():
    body = build_query_body()
    assert body == {'query': {'match_all': {}}, 'from': 0, 'size': 20}


non_implemented_params = ['published_after', 'region', 'similarity_method']


@pytest.mark.parametrize('non_implemented_param', non_implemented_params)
def test_build_query_body_params_not_implemented(non_implemented_param):
    with pytest.raises(NotImplementedError):
        build_query_body(**{non_implemented_param: ''})


def test_build_query_body_params_invalid_combination():
    with pytest.raises(InvalidInputParameterCombination):
        build_query_body(sort='', random=True)


def test_build_query_body_all_implemented_params(monkeypatch):
    params = json.load(open("test_clients_elastic/data/param_examples.json"))

    # test all with sort param separately to all with random param (cant specify both)
    val_params = {
        'media_type': params['media_type']['validated'],
        'sort': params['sort']['validated'],
        'max_duration': params['max_duration']['validated'],
        'categories': params['categories']['validated'],
        'limit': params['limit']['validated'],
        'offset': params['offset']['validated']
    }
    body = build_query_body(**val_params)
    expected = {
        'query': {
            'bool': {
                'filter': [
                    {'term': {'mediaType': 'audio'}},
                    {'term': {'mediaType': 'video'}},
                    {'range': {'duration': {'lte': 100}}},
                    {'nested': {'path': 'genres', 'query': {'match': {'genres.key': 'music'}}}},
                    {'nested': {'path': 'genres', 'query': {'match': {'genres.key': 'comedy'}}}}
                ]
            }
        },
        'sort': ['duration', 'publicationDate', 'masterBrand',
                 {'duration': {'order': 'desc'}},
                 {'publicationDate': {'order': 'desc'}},
                 {'masterBrand': {'order': 'desc'}}],
        'from': 10,
        'size': 10
    }
    assert body == expected

    # test all with random param
    val_params = {
        'media_type': params['media_type']['validated'],
        'random': params['random']['validated'],
        'max_duration': params['max_duration']['validated'],
        'categories': params['categories']['validated'],
        'limit': params['limit']['validated'],
        'offset': params['offset']['validated']
    }

    monkeypatch.setattr(get_content, 'randint', lambda *_: 1)
    body = build_query_body(**val_params)
    expected = {
        'query': {
            'bool': {
                'filter': [
                    {'term': {'mediaType': 'audio'}},
                    {'term': {'mediaType': 'video'}},
                    {'range': {'duration': {'lte': 100}}},
                    {'nested': {'path': 'genres', 'query': {'match': {'genres.key': 'music'}}}},
                    {'nested': {'path': 'genres', 'query': {'match': {'genres.key': 'comedy'}}}}
                ],
                'must': [{'function_score': {'functions': [{'random_score': {'seed': 1}}]}}]
            }
        },
        'from': 10,
        'size': 10
    }
    assert body == expected
