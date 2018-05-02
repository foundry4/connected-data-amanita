"""Application-wide python constants"""
import os

### DEFAULTS ###
# QUERY #
DEFAULT_QUERY_LIMIT = 20
DEFAULT_QUERY_OFFSET = 0
# DATABASE #
DEFAULT_DB_ENDPOINT = 'http://localhost:9200'
DEFAULT_DB_USER = 'elastic'
DEFAULT_DB_PASS = 'changeme'
DEFAULT_DB_CLIENT = 'elasticsearch'
# HTTP API #
DEFAULT_HTTP_PORT = "5001"
# GRPC API #
DEFAULT_RPC_PORT = "50051"
DEFAULT_GRPC_MAX_WORKERS = "10"

### VARS ###
# SPARQL #
"""separating char to use when converting string of tags in results to python list cant use comma as some tags have a 
comma in """
SPARQL_TAG_SEPARATOR = '^'
# GRPC #
ONE_DAY_IN_SECONDS = 60 * 60 * 24
MAX_WORKERS = int(os.getenv("MAX_WORKERS", DEFAULT_GRPC_MAX_WORKERS))
GRPC_PORT = int(os.getenv("RPC_PORT", DEFAULT_RPC_PORT))
# HTTP #
HTTP_PORT = int(os.getenv("RPC_PORT", DEFAULT_HTTP_PORT))
# LOGGING #
LOG_LEVEL = 'DEBUG'
# DATABASE #
DB_ENDPOINT = os.getenv('DB_ENDPOINT', DEFAULT_DB_ENDPOINT)
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_CLIENT = os.getenv('DB_CLIENT', DEFAULT_DB_CLIENT)


