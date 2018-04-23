import json

import pytest

import inspect

import app.api as api
from app.clients.elastic.client import ESClient
from app.clients.elastic.querybuilder.get_content import build_query_body
from app.clients.elastic.querybuilder import get_content
# response processing
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
    expected_params = list(inspect.signature(build_query_body).parameters)

    # test with sort param separately to random param (cant specify both)
    val_params = {k: v['validated'] for k, v in params.items() if
                  k not in non_implemented_params and k in expected_params and k != 'random'}
    body = build_query_body(**val_params)
    assert body == {
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

    #test random param
    val_params = {k: v['validated'] for k, v in params.items() if
                  k not in non_implemented_params and k in expected_params and k != 'sort'}
    monkeypatch.setattr(get_content, 'randint', lambda *_: 1)
    body = build_query_body(**val_params)
    assert body == {
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

