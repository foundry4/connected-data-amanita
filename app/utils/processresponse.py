from app.utils import constants
from app.utils.conversions import lower_camel_case_to_upper
from exceptions.queryexceptions import InvalidQueryResponse


def get_bindings_from_response(response):
    """Check for and receive a set of results bindings from an rdflib results object"""
    try:
        bindings = response['results']['bindings']
    except (KeyError, TypeError):
        raise InvalidQueryResponse('The query has returned an invalid response: %s' % response)
    if not isinstance(bindings, list):
        raise InvalidQueryResponse('The query has returned invalid bindings: %s' % response)
    return bindings


def transform_bindings(bindings):
    """
    Process results bindings into the format specified by the API specs.

    Changes the keys from lowerCamelCase to UpperCamelCase and removes extraneous type information.
    """
    results = []
    for item in bindings:
        item_processed = {}

        tag_fields = ['tags', 'taguris', 'tagsources', 'tagconfs']
        genre_fields = ['topLevelGenreUris', 'secondLevelGenreUris', 'thirdLevelGenreUris', 'topLevelGenres',
                        'secondLevelGenres', 'thirdLevelGenres', 'topLevelGenreKeys',
                        'secondLevelGenreKeys', 'thirdLevelGenreKeys']
        # general
        for field, data in item.items():
            if field not in tag_fields + genre_fields:
                item_processed[lower_camel_case_to_upper(field)] = data['value']

        # tags
        tags_raw = [convert_csv_to_list(item[key]['value']) for key in tag_fields]
        item_processed['Tags'] = generate_tag_list(*tags_raw)

        # genres
        genres_raw = [convert_csv_to_list(item[key]['value']) if key in item else None for key in genre_fields]
        if any(genres_raw):
            item_processed['Genres'] = generate_genre_dict(*genres_raw)
        results.append(item_processed)
    return results


def generate_tag_list(tag_names, tag_uris, tag_sources, tag_confidences):
    """Given lists of tags & properties, represent the tags/properties in the structure defined in the API
    specifications."""
    tags_by_source = []
    for source in sorted(set(tag_sources)):
        tags_by_source.append({
            'Source': source,
            'TagList': remove_duplicates_from_results_and_sort([{
                'Uri': taguri,
                'Label': tag,
                'Confidence': float(conf)
            } for tag, taguri, sourceiter, conf in zip(tag_names, tag_uris, tag_sources, tag_confidences)
                if sourceiter == source])
        })
    return tags_by_source


def generate_genre_dict(uris_1, uris_2, uris_3, names_1, names_2, names_3, keys_1, keys_2, keys_3):
    """Given lists of genres and properties, represent them in the structure defined in the API specifications."""
    genres = {}
    if uris_1 is not None:
        genres['TopLevel'] = remove_duplicates_from_results_and_sort([{
            'Uri': uri,
            'Label': name,
            'Key': key
        } for uri, name, key in zip(uris_1, names_1, keys_1)])
    if uris_2 is not None:
        genres['SecondLevel'] = remove_duplicates_from_results_and_sort([{
            'Uri': uri,
            'Label': name,
            'Key': key
        } for uri, name, key in zip(uris_2, names_2, keys_2)])
    if uris_3 is not None:
        genres['ThirdLevel'] = remove_duplicates_from_results_and_sort([{
            'Uri': uri,
            'Label': name,
            'Key': key
        } for uri, name, key in zip(uris_3, names_3, keys_3)])
    return genres


def convert_csv_to_list(csv):
    return csv.split(constants.TAG_SEPARATOR)


def is_result_set_empty(sparql_result):
    """
    This function is a workaround for a current bug in the way an empty result set is returned: Check for special case
    where result is [{"Tags":""}] instead of an empty list.

    Args:
        sparql_result (SPARQL result object)

    Returns:
        is_empty (boolean): True if results are empty
    """
    try:
        # check if first field has None value
        is_empty = next(iter(sparql_result))[0] is None
    except StopIteration:
        is_empty = True
    return is_empty


def remove_duplicates_from_results_and_sort(results):
    """
    The `GROUP_CONCAT` SPARQL operator returns duplicates that are not present in the CG, remove them. Sort the results
    too as otherwise the order is unpredictable and tests fail.
    """

    # I have tried refactoring the query to use multiple subqueries but I couldn't get UNION to return the correct
    # results.
    # In addition, using `distinct` in group concat has two issues:
    # 1) it will remove the tag source info which will contain valid duplicates eg ['mango',' mango', 'starfruit']
    # 2) it messes with the ordering of results

    # As content of dicts in list are unknown, sort by all values cast to a string. Expensive but ensures flexibility.
    if isinstance(results[0], dict):
        dupes_rm = [dict(t) for t in set([tuple(d.items()) for d in results])]
        res_sorted = sorted(dupes_rm, key=lambda x: str(x.values()))
    else:
        dupes_rm = list(set(results))
        res_sorted = sorted(dupes_rm)
    return res_sorted

