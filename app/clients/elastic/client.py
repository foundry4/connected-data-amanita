from elasticsearch5 import Elasticsearch

from app.clients.elastic.querybuilder import get_content, get_similar, get_item
from app.clients.client_superclass import DBClient
from app.clients.elastic import query_parameter_mappers
from app.clients.elastic.process_response import map_hits_to_api_spec
from exceptions.clientexceptions import NoResultsFoundError


class ESClient(DBClient):
    @property
    def parameter_definitions(self):
        return query_parameter_mappers

    def setup_connection(self):  # pragma: no cover
        store = Elasticsearch(hosts=[self.endpoint], http_auth=(self.user, self.passwd))
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

    def query(self, query, **params):  # pragma: no cover
        return self.store.search(body=query, **params)

    def close_connection(self):
        # handled by garbage collection
        pass
