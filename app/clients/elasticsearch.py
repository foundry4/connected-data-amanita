from elasticsearch5 import Elasticsearch

from app.clients.db_interface import DBClient
from app.querybuilder.elastic import get_content


class ESClient(DBClient):
    def setup_connection(self):
        store = Elasticsearch(hosts=[self.endpoint], http_auth=(self.user, self.passwd))
        self.store = store

    def get_content(self, validated_query_params):
        query_body = get_content.build_query_body(**validated_query_params)
        res = self.store.search(index='pips', doc_type='clip', body=query_body, scroll='1m')
        pass

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
