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
    Munge bindings to into the format specified by the API specs.

    Changes the keys from lowerCamelCase to UpperCamelCase and removes extraneous type information.
    """
    results = []
    for item in bindings:
        item_munged = {}
        for field, data in item.items():
            if field == 'tags':
                data['value'] = convert_csv_to_list(data['value'])
            item_munged[lower_camel_case_to_upper(field)] = data['value']
        results.append(item_munged)
    return results


def convert_csv_to_list(csv):
    return csv.split('^')


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
