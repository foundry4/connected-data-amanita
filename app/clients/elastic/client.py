from elasticsearch5 import Elasticsearch

from app.clients.db_interface import DBClient
from app.clients.elastic.querybuilder import get_content
from app.utils.conversions import lower_camel_case_to_upper


class ESClient(DBClient):
    def setup_connection(self):
        store = Elasticsearch(hosts=[self.endpoint], http_auth=(self.user, self.passwd))
        self.store = store

    def get_content(self, validated_query_params):
        query_body = get_content.build_query_body(**validated_query_params)
        es_res = self.store.search(index='pips', doc_type='clip', body=query_body, scroll='1m')
        hits = [clip['_source'] for clip in es_res['hits']['hits']]
        hits = [{lower_camel_case_to_upper(k): v for k, v in hit.items()} for hit in hits]

        for hit in hits:
            hit['MasterBrand'] = hit['MasterBrand']['mid']
            genres = {'TopLevel': [], 'SecondLevel': [], 'ThirdLevel': []}
            genre_mapping = {
                0:'TopLevel',
                1: 'SecondLevel',
                2: 'ThirdLevel'
            }
            for genre in hit['Genres']:
                genres[genre_mapping[genre['level']]].append({
                    'Uri': genre['uri'],
                    'Label': genre['label'],
                    'Key':genre['key']
                })
            hit['Genres'] = genres
            hit['PublicationDate'] = hit['ReleaseDate']
        fields_to_keep = ['Pid', 'MediaType', 'Duration', 'MasterBrand', 'Genres', 'Image', 'Title', 'PublicationDate']
        hits = [{k: v for k, v in hit.items() if k in fields_to_keep} for hit in hits]
        return {'Results': hits}

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
