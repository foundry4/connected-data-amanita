"""Application-wide python constants"""

DEFAULT_QUERY_LIMIT = 20
DEFAULT_QUERY_OFFSET = 0

DEFAULT_STARDOG_ENDPOINT = 'http://localhost:5820/content-graph/query'
DEFAULT_STARDOG_USER = 'admin'
DEFAULT_STARDOG_PASS = 'admin'

TAG_SEPARATOR = '^'  # separating char to use when converting string of tags to python list - cant use comma as some
# tags have a comma in
