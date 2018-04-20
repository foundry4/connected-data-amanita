from random import randint

from app.utils import constants
from exceptions.queryexceptions import InvalidInputParameterCombination

from elasticsearch_dsl import Search, Q


def build_query_body(media_type=None, sort=None, max_duration=None, published_after=None, categories=None,
                     region=None, random=False, limit=constants.DEFAULT_QUERY_LIMIT, similarity_method=None,
                     offset=constants.DEFAULT_QUERY_OFFSET):
    if published_after is not None:
        raise NotImplementedError('The parameter `publishedAfter` is not yet implemented')
    if region is not None:
        raise NotImplementedError('The parameter `region` is not yet implemented')
    if similarity_method is not None:
        raise NotImplementedError('The parameter `similarityMethod` is not yet implemented')
    if sort is not None and random:
        raise InvalidInputParameterCombination('Cannot specify both `sort` and `random`.')

    search = Search(index='pips')
    search = search[offset:offset + limit]  # TODO: THIS DOESNT WORK?? query builds as should but no effect
    if sort:
        search = search.sort(*sort)
    if media_type:
        for media in media_type:
            search = search.filter('term', mediaType=media)

    if max_duration:
        search = search.filter('range', duration={'lte': max_duration})

    if categories:
        for cat in categories:
            search = search.filter('nested', path='genres', query=Q('match', genres__key=cat))

    if random:
        search = search.query('function_score', functions=[{'random_score': {'seed': randint(0, 999)}}])

    return search.to_dict()
