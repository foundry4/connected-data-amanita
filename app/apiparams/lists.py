"""Lists of API Parameters for particular endpoints."""


def get_param_validators_for_endpoint(endpoint, definitions):
    if endpoint == 'content':
        return {
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
        return {
            'mediaType': definitions.media_type,
            'sort': definitions.sort,
            'maxDuration': definitions.max_duration,
            'region': definitions.region,
            'publishedAfter': definitions.published_after,
            'limit': definitions.limit,
            'offset': definitions.offset,
            'similarityMethod': definitions.similarity_method,
        }
    elif endpoint == 'item':
        return {
            'item_uri': definitions.item_uri
        }
    else:
        raise ValueError(f'{endpoint} is not a valid endpoint.')
