from elasticsearch5 import Elasticsearch

from app.clients.client_interface import DBClient
from app.clients.elastic.process_response import transform_hits
from app.clients.elastic.querybuilder import get_content, get_item, get_similar
from exceptions.clientexceptions import NoResultsFoundError


class ESClient(DBClient):
    def setup_connection(self):
        store = Elasticsearch(hosts=[self.endpoint], http_auth=(self.user, self.passwd))
        self.store = store

    def get_content(self, validated_query_params):
        query_body = get_content.build_query_body(**validated_query_params)
        es_res = self.store.search(index='pips', doc_type='clip', body=query_body, scroll='1m')
        clips = transform_hits(es_res)
        return {'Results': clips}

    def get_item(self, validated_item_uri):
        query_body = get_item.build_query_body(validated_item_uri)
        es_res = self.store.search(index='pips', doc_type='clip', body=query_body, scroll='1m')
        hits = transform_hits(es_res)
        if len(hits) == 0:
            raise NoResultsFoundError(f'No results for URI: {validated_item_uri}')
        return hits[0]

    def get_similar(self, validated_item_uri, validated_query_params):
        query_body = get_similar.build_query_body(item_uri=validated_item_uri, **validated_query_params)
        es_res = self.store.search(index='pips', doc_type='clip', body=query_body, scroll='1m')
        clips = transform_hits(es_res)
        return {'Results': clips}

    @staticmethod
    def query(query, **params):
        pass

    def close_connection(self):
        # handled by garbage collection
        pass
