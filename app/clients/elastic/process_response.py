from app.utils.conversions import lower_camel_case_to_upper


def transform_hits(es_res):
    """Transform raw ES results to align with API specification."""
    hits = [clip for clip in es_res['hits']['hits']]
    clips = []
    for hit in hits:
        clip = hit['_source']
        clip = {lower_camel_case_to_upper(k): v for k, v in clip.items()}
        clip['Uri'] = hit['_id']
        clip['MasterBrand'] = clip['MasterBrand']['mid'] if clip['MasterBrand'] is not None else None
        genres = {'TopLevel': [], 'SecondLevel': [], 'ThirdLevel': []}
        genre_mapping = {
            0: 'TopLevel',
            1: 'SecondLevel',
            2: 'ThirdLevel'
        }
        for genre in clip['Genres']:
            genres[genre_mapping[genre['level']]].append({
                'Uri': genre['uri'],
                'Label': genre['label'],
                'Key': genre['key']
            })
        clip['Genres'] = genres
        clip['PublicationDate'] = clip['ReleaseDate']
        clips.append(clip)

    fields_to_keep = ['Pid', 'Uri', 'MediaType', 'Duration', 'MasterBrand', 'Genres', 'Image', 'Title', 'PublicationDate']
    hits = [{k: v for k, v in clip.items() if k in fields_to_keep} for clip in clips]
    return hits
