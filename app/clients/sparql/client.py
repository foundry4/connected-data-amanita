import json
from urllib.error import HTTPError, URLError

from flask import logging
from rdflib import Graph
from rdflib.namespace import NamespaceManager
from rdflib.plugins.stores import sparqlstore

from app.clients.client_interface import DBClient
from app.clients.sparql import query_param_definitions
from app.clients.sparql.querybuilder import get_content, get_similar
from app.clients.sparql.querybuilder import get_item
from app.clients.sparql.namespaces import namespaces as ns
from app.clients.sparql.process_response import get_bindings_from_response, transform_bindings, is_result_set_empty
from exceptions.clientexceptions import NoResultsFoundError, DBClientResponseError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SPARQLClient(DBClient):
    @property
    def client_name(self):
        return 'stardog'

    @property
    def parameter_definitions(self):
        return query_param_definitions

    def setup_connection(self):
        store = sparqlstore.SPARQLUpdateStore()
        store.setCredentials(self.user, self.passwd)
        store.open((self.endpoint, self.endpoint))
        self.store = store
        self._initialise_namespaces()

    def get_content(self, validated_query_params):
        query_string = get_content.build_query(**validated_query_params)
        sparql_result = self.query(query_string)
        if is_result_set_empty(sparql_result):
            bindings = []
        else:
            result_serialized = json.loads(sparql_result.serialize(format='json'))
            bindings = get_bindings_from_response(result_serialized)
        content_list = transform_bindings(bindings)
        return content_list

    def get_item(self, validated_item_uri):
        query_string = get_item.build_query(validated_item_uri)
        sparql_result = self.query(query_string)
        if is_result_set_empty(sparql_result):
            raise NoResultsFoundError(f'No results for URI: {validated_item_uri}')
        else:
            result_serialized = json.loads(sparql_result.serialize(format='json'))
            bindings = get_bindings_from_response(result_serialized)
        item_list = transform_bindings(bindings)
        item = item_list[0]
        item['Uri'] = str(validated_item_uri)
        return item

    def get_similar(self, validated_item_uri, validated_query_params):
        query_string = get_similar.build_query(item_uri=validated_item_uri, **validated_query_params)
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
