from abc import ABC, abstractmethod


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
    def get_content(self, mapped_params):
        """
        Get list of content from graph and filter based on `query_params`.
        Args:
            mapped_params (dict): parameters for filtering results
        """

    @abstractmethod
    def get_item(self, mapped_params):
        """
        Get list of content from graph and filter based on `query_params`.
        Args:
            mapped_params (dict): parameters for filtering results, should include 'itemUri'
        """

    @abstractmethod
    def get_similar(self, mapped_params):
        """
        Get list of content related to given item uri and filter based on `query_params`.
        Args:
            mapped_params (dict): parameters for filtering results, should include 'itemUri'
        """


