from app.utils.conversions import lower_camel_case_to_upper


def transform_hits(es_res):
    hits = [clip['_source'] for clip in es_res['hits']['hits']]
    hits = [{lower_camel_case_to_upper(k): v for k, v in hit.items()} for hit in hits]
    for hit in hits:
        hit['MasterBrand'] = hit['MasterBrand']['mid'] if hit['MasterBrand'] is not None else None
        genres = {'TopLevel': [], 'SecondLevel': [], 'ThirdLevel': []}
        genre_mapping = {
            0: 'TopLevel',
            1: 'SecondLevel',
            2: 'ThirdLevel'
        }
        for genre in hit['Genres']:
            genres[genre_mapping[genre['level']]].append({
                'Uri': genre['uri'],
                'Label': genre['label'],
                'Key': genre['key']
            })
        hit['Genres'] = genres
        hit['PublicationDate'] = hit['ReleaseDate']
    fields_to_keep = ['Pid', 'MediaType', 'Duration', 'MasterBrand', 'Genres', 'Image', 'Title', 'PublicationDate']
    hits = [{k: v for k, v in hit.items() if k in fields_to_keep} for hit in hits]
    hits = {'Results': hits}
    return hits
