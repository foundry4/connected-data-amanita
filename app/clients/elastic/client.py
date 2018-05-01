from elasticsearch5 import Elasticsearch

from app.clients.elastic.querybuilder import get_content, get_similar, get_item
from app.clients.client_superclass import DBClient

from app.clients.elastic.query_parameter_mappers import http as http_param_mappings, rpc as rpc_param_mappings
from app.clients.elastic.process_response import map_hits_to_api_spec
from exceptions.clientexceptions import NoResultsFoundError


class ESClient(DBClient):
    @staticmethod
    def get_parameter_definitions(request_type):
        if request_type not in ['http', 'rpc']:
            raise ValueError(f'Request type {request_type} has no parameter mappings.')
        if request_type == 'http':
            return http_param_mappings
        if request_type == 'rpc':
            return rpc_param_mappings

    def setup_connection(self):
        if hasattr(self, 'user') and hasattr(self, 'password'):
            store = Elasticsearch(hosts=[self.endpoint], http_auth=(self.user, self.passwd))
        else:
            store = Elasticsearch(hosts=[self.endpoint])
        self.store = store

    def get_content(self, mapped_params):
        query_body = get_content.build_query_body(**mapped_params)
        es_response = self.query(query_body, index='pips', doc_type='clip', scroll='1m')
        clips = map_hits_to_api_spec(es_response)
        return {'results': clips}

    def get_item(self, mapped_params):
        query_body = get_item.build_query_body(**mapped_params)
        es_response = self.query(query_body, index='pips', doc_type='clip', scroll='1m')
        clips = map_hits_to_api_spec(es_response)
        if len(clips) == 0:
            raise NoResultsFoundError(f'No results for URI: {mapped_params}')
        return clips[0]

    def get_similar(self, mapped_params):
        query_body = get_similar.build_query_body(**mapped_params)
        es_response = self.query(query_body, index='pips', doc_type='clip', scroll='1m')
        clips = map_hits_to_api_spec(es_response)
        return {'results': clips}

    def query(self, query, **params):
        return self.store.search(body=query, **params)

    def close_connection(self):
        # handled by garbage collection
        pass
