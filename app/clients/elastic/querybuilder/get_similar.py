from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MoreLikeThis, Q
from app.utils import constants


def build_query_body(item_uri=None, media_type=None, max_duration=None, published_after=None,
                     region=None, similarity_method=None, limit=constants.DEFAULT_QUERY_LIMIT,
                     offset=constants.DEFAULT_QUERY_OFFSET):
    """Build query dict ready to pass to Elasticsearch search instance for retrieving a list of similar items given a
    URI."""
    if published_after is not None:
        raise NotImplementedError('The parameter `publishedAfter` is not yet implemented.')
    if region is not None:
        raise NotImplementedError('The parameter `region` is not yet implemented.')
    if similarity_method is not None:
        raise NotImplementedError('The parameter `similarityMethod` is not yet implemented for ES.')

    search = Search(index='pips')
    search = search[offset:offset + limit]  # TODO: THIS DOESNT WORK?? query builds as should but no effect

    if media_type:
        for media in media_type:
            search = search.filter('term', mediaType=media)

    if max_duration:
        search = search.filter('range', duration={'lte': max_duration})

    similarity_filters = [
        # by title
        MoreLikeThis(
            like={'_index': 'pips', '_type': 'clip', '_id': item_uri},
            fields=['title', 'masterBrand.mid', 'mediaType'],
            min_term_freq=1,
            min_doc_freq=1
        ),
        Q(
            'nested',
            path='genres',
            query=MoreLikeThis(
                fields=['genres.key'],
                like={'_index': 'pips', '_type': 'clip', '_id': item_uri},
                min_term_freq=1,
                min_doc_freq=1
            )
        )
    ]
    search = search.query('bool', should=similarity_filters)

    return search.to_dict()
