"""Application-wide python constants"""

DEFAULT_QUERY_LIMIT = 20
DEFAULT_QUERY_OFFSET = 0

DEFAULT_DB_ENDPOINT = 'http://localhost:9200'
DEFAULT_DB_USER = 'elastic'
DEFAULT_DB_PASS = 'changeme'

SPARQL_TAG_SEPARATOR = '^'  # separating char to use when converting string of tags in results to python list
# cant use comma as some tags have a comma in
DEFAULT_HTTP_PORT = "5001"

DEFAULT_RPC_PORT = "50051"
DEFAULT_GRPC_MAX_WORKERS = "10"

DEFAULT_DB_CLIENT = 'elasticsearch'

LOG_LEVEL = 'DEBUG'
