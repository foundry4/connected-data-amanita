from abc import ABC, abstractmethod

from app.apiparams.mapping import map_param_values_to_db_compatible
from app.utils.conversions import map_multidict_to_dict


class DBClient(ABC):
    def __init__(self, endpoint, user, passwd):
        """
        Defines public interface for a database client object. New clients should inherit from this class.

        Args:
            endpoint (string): endpoint URL for stardog instance
            user (string): username for HTTP Stardog auth
            passwd (string): password for HTTP auth

        Attributes:
            endpoint (string): endpoint URL for stardog instance
            user (string): username for HTTP Stardog auth
            passwd (string): password for HTTP auth
            store (SPARQLUpdateStore): object for accessing SPARQL endpoint
        """

        self.endpoint = endpoint
        self.user = user
        self.passwd = passwd
        self.store = None
        self.setup_connection()

    @property
    @abstractmethod
    def parameter_definitions(self):
        """Store the parameter definitions specific to the client as a property."""

    @abstractmethod
    def setup_connection(self):  # pragma: no cover
        """Uses authentication credentials to open connection to SPARQL store."""

    @abstractmethod
    def close_connection(self):
        """Close connection to database."""

    @staticmethod
    @abstractmethod
    def query(query, **params):
        """
        Query the SPARQL store object.

        Args:
            query (string): SPARQL query to send to endpoint
            params (dict): any additional arguments to be passed to query function
        """

    @abstractmethod
    def get_content(self, validated_query_params):
        """
        Get list of content from graph and filter based on `query_params`.
        Args:
            validated_query_params (dict): _validated_ query parameters for filtering results
        """

    @abstractmethod
    def get_item(self, validated_item_uri):
        """
        Get list of content from graph and filter based on `query_params`.
        Args:
            validated_item_uri (rdflib.URIRef): _validated_ uri of item to get data for
        """

    @abstractmethod
    def get_similar(self, validated_item_uri, validated_query_params):
        """
        Get list of content related to given item uri and filter based on `query_params`.
        Args:
            validated_query_params: _validated_ query parameters for filtering results
            validated_item_uri (rdflib.URIRef): _validated_ uri of item to get data for
        """

    # parameter mapping
    def map_content_query_params_to_db_compatible(self, query_params):
        """Process input multidict of params from inbound query to regular dict of params that has
        been validated against a list of expected params and values.

        Arguments:
            query_params (MultiDict): query parameters from HTTP request

        Returns:
            validated_typed_params (dict): parameters that have been validated and cast to the correct type
        """
        query_params_dict = map_multidict_to_dict(query_params)
        validated_typed_params = map_param_values_to_db_compatible(query_params_dict, endpoint='content',
                                                                   parameter_definitions=self.parameter_definitions)
        return validated_typed_params

    def map_item_query_uri_to_db_compatible(self, uri):
        """Convert URI into format compatible with database."""
        params = {'itemUri': uri}
        validated = map_param_values_to_db_compatible(params, endpoint='item',
                                                      parameter_definitions=self.parameter_definitions)
        return validated['item_uri']

    def map_similar_query_params_to_db_compatible(self, query_params):
        """Process input multidict of params from inbound query to regular dict of params that has
        been validated against a list of expected params and values.

        Arguments:
            query_params (MultiDict): query parameters from HTTP request

        Returns:
            validated_typed_params (dict): parameters that have been validated and cast to the correct type
        """
        query_params_dict = map_multidict_to_dict(query_params)
        validated_typed_params = map_param_values_to_db_compatible(query_params_dict, endpoint='similar',
                                                                   parameter_definitions=self.parameter_definitions)
        return validated_typed_params
