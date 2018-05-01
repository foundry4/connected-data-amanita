from copy import copy

from app.services import amanita_pb2


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

        if 'href' in clip['version']:
            del clip['version']['href']
        clips.append(clip)

    fields_to_keep = ['pid', 'uri', 'mediaType', 'duration', 'masterBrand', 'genres', 'image', 'title',
                      'publicationDate', 'version']
    hits = [{k: v for k, v in clip.items() if k in fields_to_keep} for clip in clips]
    return hits


def map_client_results_to_proto(client_res):
    mapped_items = []
    for item in client_res['results']:
        mapped_item = amanita_pb2.MinimalItem(
            master_brand=item['masterBrand'],
            media_type=item['mediaType'].upper(),
            genres={
                {
                    'topLevel': 'top_level',
                    'secondLevel': 'second_level',
                    'thirdLevel': 'third_level'
                }
                [level]:
                    [
                        amanita_pb2.Genre(
                            uri=genre['uri'],
                            label=genre['label'],
                            key=genre['key']
                        )
                        for genre in genres
                    ]
                for level, genres in item['genres'].items()
            },
            pid=item['pid'],
            title=item['title'],
            version=amanita_pb2.Version(
                duration=item['version']['duration'],
                pid=item['version']['pid']
            ),
            duration=item['duration'],
            uri=item['uri'],
            publication_date=item['publicationDate'],
            image=item['image']
        )
        mapped_items.append(mapped_item)

    mapped_result = amanita_pb2.ResultSet(
        results=mapped_items
    )
    return mapped_result
