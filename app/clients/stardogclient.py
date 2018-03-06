import logging
from urllib.error import HTTPError, URLError

from rdflib.plugins.stores import sparqlstore

from app.clients.sparqlclient import SPARQLClient
from exceptions.clientexceptions import DBClientResponseError

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)


class StardogClient(SPARQLClient):

    def setup_connection(self):
        store = sparqlstore.SPARQLUpdateStore()
        store.setCredentials(self.user, self.passwd)
        store.open((self.endpoint, self.endpoint))
        return store

    def query(self, query, **params):
        try:
            return self.store.query(query, **params)
        except (HTTPError, URLError) as e:
            logger.error(e)
            logger.debug(f"Query string sent:\n{query}")
            raise DBClientResponseError("Error querying upstream graph store")
