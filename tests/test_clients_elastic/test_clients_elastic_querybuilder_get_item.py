from app.clients.elastic.querybuilder.get_item import build_query_body

# response processing


# query building
def test_query_building_no_params():
    body = build_query_body('item_uri')
    expected = {'query': {'term': {'_id': 'item_uri'}}}
    assert body == expected


