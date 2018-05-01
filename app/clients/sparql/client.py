import json
from urllib.error import HTTPError, URLError

from rdflib import Graph
from rdflib.namespace import NamespaceManager
from rdflib.plugins.stores import sparqlstore

from app.clients.client_superclass import DBClient

from app.clients.sparql.query_parameter_mappers import http as http_params
from app.clients.sparql.namespaces import namespaces as ns
from app.clients.sparql.process_response import get_bindings_from_response, transform_bindings, is_result_set_empty
from app.clients.sparql.querybuilder import get_content, get_similar
from app.clients.sparql.querybuilder import get_item
from app.utils import logging
from exceptions.clientexceptions import NoResultsFoundError, DBClientResponseError

logger = logging.get_logger(__name__)


class SPARQLClient(DBClient):
    @staticmethod
    def get_parameter_definitions(request_type):
        return http_params

    def setup_connection(self):
        store = sparqlstore.SPARQLUpdateStore()
        store.setCredentials(self.user, self.passwd)
        store.open((self.endpoint, self.endpoint))
        self.store = store
        self._initialise_namespaces()

    def get_content(self, mapped_params):
        query_string = get_content.build_query(**mapped_params)
        sparql_result = self.query(query_string)
        if is_result_set_empty(sparql_result):
            bindings = []
        else:
            result_serialized = json.loads(sparql_result.serialize(format='json'))
            bindings = get_bindings_from_response(result_serialized)
        content_list = transform_bindings(bindings)
        return content_list

    def get_item(self, mapped_params):
        query_string = get_item.build_query(**mapped_params)
        sparql_result = self.query(query_string)
        if is_result_set_empty(sparql_result):
            raise NoResultsFoundError(f'No results for URI: {mapped_params["item_uri"]}')
        else:
            result_serialized = json.loads(sparql_result.serialize(format='json'))
            bindings = get_bindings_from_response(result_serialized)
        item_list = transform_bindings(bindings)
        item = item_list[0]
        item['uri'] = str(mapped_params['item_uri'])
        return item

    def get_similar(self, mapped_params):
        query_string = get_similar.build_query(**mapped_params)
        sparql_result = self.query(query_string)
        if is_result_set_empty(sparql_result):
            bindings = []
        else:
            result_serialized = json.loads(sparql_result.serialize(format='json'))
            bindings = get_bindings_from_response(result_serialized)
        content_list = transform_bindings(bindings)
        return content_list

    def close_connection(self):
        self.store.close()

    def query(self, query, **params):
        try:
            return self.store.query(query, **params)
        except (HTTPError, URLError) as e:
            logger.error(e)
            logger.debug(f"Query string sent:\n{query}")
            raise DBClientResponseError("Error querying upstream graph store")

    def _initialise_namespaces(self):
        ns_manager = NamespaceManager(Graph(self.store))
        for namespace in ns.items():
            ns_manager.bind(*namespace)
