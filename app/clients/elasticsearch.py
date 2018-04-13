from elasticsearch5 import Elasticsearch

from app.clients.db_interface import DBClient


class ESClient(DBClient):
    def setup_connection(self):
        store = Elasticsearch(hosts=[self.endpoint], http_auth=(self.user, self.passwd))
        self.store = store

    def get_content(self, validated_query_params):
        res = self.store.get(index='pips', doc_type='clip')
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
