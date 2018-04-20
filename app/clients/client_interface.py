from abc import ABC, abstractmethod

# todo: turn this into client handler - specifies interface and chooses client to use

from app.apiparams.lists import get_param_validators_for_endpoint
from app.utils.conversions import map_multidict_to_dict
from exceptions.queryexceptions import InvalidInputParameter, InvalidInputParameterValue, InvalidInputQuery


class DBClient(ABC):
    """
    """

    def __init__(self, endpoint, user, passwd):
        """
        Defines public interface for a graph client object. For now the object is limited to setting up a connection
        and querying the SPARQL endpoint, with the `get_content` method forming a particular SPAQRL query to list
        content and process optional parameters.

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
        """DOCSTRING TODO"""

    @abstractmethod
    def setup_connection(self):
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

    # parameter validation
    def process_content_query_params(self, query_params):
        """Process input multidict of params from inbound query to regular dict of params that has
        been validated against a list of expected params and values.

        Arguments:
            query_params (MultiDict): query parameters from HTTP request

        Returns:
            validated_typed_params (dict): parameters that have been validated and cast to the correct type
        """
        query_params_dict = map_multidict_to_dict(query_params)
        validated_typed_params = self._validate_param_dict(query_params_dict, endpoint='content')
        return validated_typed_params

    def process_item_query_uri(self, uri):
        """Convert URI into format compatible with rdflib."""
        params = {'itemUri':uri}
        validated = self._validate_param_dict(params, endpoint='item')
        return validated['item_uri']

    def process_similar_query_params(self, query_params):
        """Process input multidict of params from inbound query to regular dict of params that has
        been validated against a list of expected params and values.

        Arguments:
            query_params (MultiDict): query parameters from HTTP request

        Returns:
            validated_typed_params (dict): parameters that have been validated and cast to the correct type
        """
        query_params_dict = map_multidict_to_dict(query_params)
        validated_typed_params = self._validate_param_dict(query_params_dict, endpoint='similar')
        return validated_typed_params

    def _validate_param_dict(self, query_params, endpoint):
        """Iterate through parameters, validate them and cast them to the correct type."""
        validated_typed_params, exceptions = {}, []
        validators = get_param_validators_for_endpoint(endpoint, self.parameter_definitions)
        for param_name, param_val in query_params.items():
            try:
                try:
                    validator = validators[param_name]
                except KeyError:
                    raise InvalidInputParameter(
                        f'Parameter `{param_name}` is not included in the defined parameters {list(validators)}'
                    )
                validated_typed_params[validator.snake_case_name] = validator.validate(param_val)
            except (InvalidInputParameter, InvalidInputParameterValue) as e:
                exceptions.append(f'{type(e).__name__}: {str(e)}')

        if exceptions:
            raise InvalidInputQuery("Invalid parameters/value(s):\n    %s" % '\n    '.join(exceptions))

        return validated_typed_params

