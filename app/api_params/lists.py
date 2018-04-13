"""Lists of API Parameters for particular endpoints."""
import os

from app.api_params import rdf_definitions, es_definitions
from app.utils import constants

DB_CLIENT = os.getenv('DB_CLIENT', constants.DEFAULT_DB_CLIENT)
if DB_CLIENT == 'stardog':
    defs = rdf_definitions
elif DB_CLIENT == 'elasticsearch':
    defs = es_definitions
else:
    raise ValueError(f"No such database: {DB_CLIENT}.")

list_content_query_parameter_validators = {
    'mediaType': defs.media_type,
    'sort': defs.sort,
    'maxDuration': defs.max_duration,
    'region': defs.region,
    'publishedAfter': defs.published_after,
    'categories': defs.categories,
    'tags': defs.tags,
    'limit': defs.limit,
    'offset': defs.offset,
    'random': defs.random
}
list_similar_query_parameter_validators = {
    'mediaType': defs.media_type,
    'sort': defs.sort,
    'maxDuration': defs.max_duration,
    'region': defs.region,
    'publishedAfter': defs.published_after,
    'limit': defs.limit,
    'offset': defs.offset,
    'similarityMethod': defs.similarity_method,
}
