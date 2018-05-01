from copy import copy


def map_hits_to_api_spec(es_res):
    """Transform raw ES results to align with API specification."""
    hits = es_res['hits']['hits']
    clips = []
    for hit in hits:
        clip = copy(hit['_source'])
        clip['uri'] = hit['_id']
        clip['masterBrand'] = clip['masterBrand']['mid'] if clip['masterBrand'] is not None else None
        genres = {'topLevel': [], 'secondLevel': [], 'thirdLevel': []}
        genre_mapping = {
            0: 'topLevel',
            1: 'secondLevel',
            2: 'thirdLevel'
        }
        for genre in clip['genres']:
            genres[genre_mapping[genre['level']]].append({
                'uri': genre['uri'],
                'label': genre['label'],
                'key': genre['key']
            })
        clip['genres'] = genres
        clip['publicationDate'] = clip['releaseDate']
        clip['version'] = clip['version']['pid']
        clips.append(clip)

    fields_to_keep = ['pid', 'uri', 'mediaType', 'duration', 'masterBrand', 'genres', 'image', 'title',
                      'publicationDate', 'version']
    hits = [{k: v for k, v in clip.items() if k in fields_to_keep} for clip in clips]
    return hits
