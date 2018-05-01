from elasticsearch_dsl import Search


def build_query_body(item_uri):
    """Build query dict ready to pass to Elasticsearch search instance for retrieving a single item by URI."""
    search = Search(index='pips').query('term', _id=item_uri)

    return search.to_dict()
