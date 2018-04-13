import json

from elasticsearch5 import Elasticsearch

from app.clients.db_interface import DBClient


class ESClient(DBClient):

    def setup_connection(self):
        pass

    @staticmethod
    def query(query, **params):
        pass

    def get_content(self, validated_query_params):
        pass

    def get_item(self, validated_item_uri):
        pass

    def get_similar(self, validated_item_uri, validated_query_params):
        pass

    def initialise_namespaces(self):
        pass
