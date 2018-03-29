"""Lists of API Parameters for particular endpoints."""
from app.api_params.definitions import media_type, sort, max_duration, region, published_after, categories, tags, \
    limit, offset, random, similarity_method

list_content_query_parameter_validators = {
    'mediaType': media_type,
    'sort': sort,
    'maxDuration': max_duration,
    'region': region,
    'publishedAfter': published_after,
    'categories': categories,
    'tags': tags,
    'limit': limit,
    'offset': offset,
    'random': random
}
list_similar_query_parameter_validators = {
    'mediaType': media_type,
    'sort': sort,
    'maxDuration': max_duration,
    'region': region,
    'publishedAfter': published_after,
    'limit': limit,
    'offset': offset,
    'similarityMethod': similarity_method,
}
