from app.querybuilder.elastic.subqueries import build_sort_statement, update_dict_recursively, build_filter_body, \
    build_must_body, build_bool_queries
from app.utils import constants
from exceptions.queryexceptions import InvalidInputParameterCombination


def build_query_body(media_type=None, sort=None, max_duration=None, published_after=None, categories=None,
                     region=None, random=False, limit=constants.DEFAULT_QUERY_LIMIT,
                     offset=constants.DEFAULT_QUERY_OFFSET):
    if published_after is not None:
        raise NotImplementedError('The parameter `publishedAfter` is not yet implemented')
    if region is not None:
        raise NotImplementedError('The parameter `region` is not yet implemented')
    if sort is not None and random:
        raise InvalidInputParameterCombination('Cannot specify both `sort` and `random`.')

    body = {
        'size': limit,
        'from': offset,
        'sort': build_sort_statement(sort)
    }

    if media_type:
        # todo: reingest data to make Video->video in es db
        media_query = build_bool_queries([('term', 'mediaType', media.title()) for media in media_type])
        update_dict_recursively(body, ['query', 'bool', 'should'], media_query)

    if max_duration:
        duration_query = build_bool_queries([('range', 'duration', max_duration)])
        update_dict_recursively(body, ['query', 'bool', 'filter'], duration_query)

    if categories:
        update_dict_recursively(body, ['query', 'nested'], {
            'path': 'genres',
            'score_mode': 'avg',
            'query': {
                'bool': {
                    'must': build_bool_queries([('match', 'genres.key', cat) for cat in categories])
                }
            }
        })

    return body
