import json

from rdflib import Graph
from rdflib.namespace import NamespaceManager

from app.clients.graphclient import GraphClient
from app.querybuilder.sparql import get_content, get_item, get_similar
from app.utils.namespaces import namespaces as ns
from app.utils.processresponse import get_bindings_from_response, transform_bindings, is_result_set_empty
from exceptions.clientexceptions import NoResultsFoundError


# noinspection PyAbstractClass

class SPARQLClient(GraphClient):

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
        item['Programme'] = str(validated_item_uri)
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

    def initialise_namespaces(self):
        ns_manager = NamespaceManager(Graph(self.store))
        for namespace in ns.items():
            ns_manager.bind(*namespace)
