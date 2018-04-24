"""Application-wide python constants"""

DEFAULT_QUERY_LIMIT = 20
DEFAULT_QUERY_OFFSET = 0

DEFAULT_DB_ENDPOINT = 'http://localhost:5820/content-graph/query'
DEFAULT_DB_USER = 'admin'
DEFAULT_DB_PASS = 'admin'

TAG_SEPARATOR = '^'  # separating char to use when converting string of tags in results to python list
# cant use comma as some tags have a comma in
DEFAULT_HTTP_PORT = "5001"

DEFAULT_DB_CLIENT = 'stardog'

LOG_LEVEL = 'DEBUG'
