import json

from rdflib.namespace import NamespaceManager
from rdflib import Graph

from app.clients.graphclient import GraphClient
from app.querybuilder import sparql
from app.utils.processresponse import get_bindings_from_response, transform_bindings, is_result_set_empty
from app.utils.namespaces import namespaces as ns


# noinspection PyAbstractClass
class SPARQLClient(GraphClient):

    def get_content(self, query_params):
        query_string = sparql.build_get_content_query(**query_params)
        sparql_result = self.query(query_string)
        if is_result_set_empty(sparql_result):
            bindings = []
        else:
            result_serialized = json.loads(sparql_result.serialize(format='json'))
            bindings = get_bindings_from_response(result_serialized)
        content_list = transform_bindings(bindings)
        return content_list

    def initialise_namespaces(self):
        ns_manager = NamespaceManager(Graph(self.store))
        for namespace in ns.items():
            ns_manager.bind(*namespace)

