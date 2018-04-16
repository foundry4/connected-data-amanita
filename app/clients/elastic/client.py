from elasticsearch5 import Elasticsearch

from app.clients.db_interface import DBClient
from app.clients.elastic.process_response import transform_hits
from app.clients.elastic.querybuilder import get_content
from app.utils.conversions import lower_camel_case_to_upper


class ESClient(DBClient):
    def setup_connection(self):
        store = Elasticsearch(hosts=[self.endpoint], http_auth=(self.user, self.passwd))
        self.store = store

    def get_content(self, validated_query_params):
        query_body = get_content.build_query_body(**validated_query_params)
        es_res = self.store.search(index='pips', doc_type='clip', body=query_body, scroll='1m')
        hits = transform_hits(es_res)
        return hits

    def get_item(self, validated_item_uri):
        pass

    def get_similar(self, validated_item_uri, validated_query_params):
        pass

    @staticmethod
    def query(query, **params):
        pass

    def close_connection(self):
        # handled by garbage collection
        pass

