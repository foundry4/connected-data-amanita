"""This file defines which parameters are used/needed for each endpoint. DB Clients to be imoplemented should
implement a `parameter_definitions` property that contains definitions of all the parameters listed here.

Returns objects to map parameter values to the correct format, given all of the mapping objects defined by the client,
and the relevant endpoint. """


def get_param_mappers_for_endpoint(endpoint, definitions):
    if endpoint == 'content':
        mappers = {
            'mediaType': definitions.media_type,
            'sort': definitions.sort,
            'maxDuration': definitions.max_duration,
            'region': definitions.region,
            'publishedAfter': definitions.published_after,
            'categories': definitions.categories,
            'limit': definitions.limit,
            'offset': definitions.offset,
            'random': definitions.random
        }
    elif endpoint == 'similar':
        mappers = {
            'itemUri': definitions.item_uri,
            'mediaType': definitions.media_type,
            'sort': definitions.sort,
            'maxDuration': definitions.max_duration,
            'region': definitions.region,
            'publishedAfter': definitions.published_after,
            'limit': definitions.limit,
            'offset': definitions.offset,
        }
    elif endpoint == 'item':
        mappers = {
            'itemUri': definitions.item_uri
        }
    else:
        raise ValueError(f'{endpoint} is not a valid endpoint.')
    return mappers
