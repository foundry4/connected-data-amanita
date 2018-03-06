from abc import ABC, abstractmethod


class GraphClient(ABC):
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
        self.store = self.setup_connection()

    @abstractmethod
    def setup_connection(self):
        """Uses authentication credentials to open connection to SPARQL store."""
        pass

    @staticmethod
    @abstractmethod
    def query(query, **params):
        """
        Query the SPARQL store object.

        Args:
            query (string): SPARQL query to send to endpoint
            params (dict): any additional arguments to be passed to query function
        """
        pass

    @abstractmethod
    def get_content(self, query_params):
        """
        Get list of content from graph and filter based on `query_params`.
        Args:
            query_params (dict): _validated_ query parameters for filtering results
        """
        pass
