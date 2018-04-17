from elasticsearch_dsl import Search


def build_query_body(item_uri):

    search = Search(index='pips').query('term', _id=item_uri)

    return search.to_dict()
