from app.utils import constants
from app.utils.namespaces import namespaces as ns


def build_get_content_query(media=None, tags=None, limit=constants.DEFAULT_QUERY_LIMIT,
                            offset=constants.DEFAULT_QUERY_OFFSET, **all_other_bindings):
    """
    Construct a SPARQL query to retrieve content from the content graph. Filter by query_params

    Arguments:
        media (Literal): type of media to be returned eg Audio, Video
        tags (list): list of Literal tags to filter by
        limit (int): number of results to return (for pagination)
        offset (int): offset of results to return (for pagination)
        all_other_bindings (dict):

    Returns:
        query_string (string): SPARQL query
    """
    tag_bindings_statement = _build_sparql_anding_statement(
        object_list=tags,
        predicate=ns['datalab']['tag'],
        programme_binding='programme'
    )
    media_bindings_statement = _build_values_oring_statement('medium', media)
    bindings_statements = _serialize_sparql_bindings(all_other_bindings)

    query_string = (f"""
        SELECT ?programme ?medium ?duration ?publicationDate ?masterbrand ?genre 
        (GROUP_CONCAT(?tag;separator="^") as ?tags)
           WHERE {{
              ?programme rdf:type datalab:PipsEntity .
              OPTIONAL {{?programme datalab:medium ?medium }} .
              OPTIONAL {{?programme po:duration ?duration }} .
              OPTIONAL {{?programme po:masterbrand ?masterbrand}} .
              BIND("genre" as ?genre) .
              OPTIONAL {{?programme datalab:tag ?tag}} .
             {tag_bindings_statement}
             {bindings_statements}
             {media_bindings_statement}
           }} 
        GROUP BY ?programme ?medium ?duration ?publicationDate ?masterbrand ?genre
        ORDER BY ASC(?programme)
        LIMIT {limit}
        OFFSET {offset}
    """)
    return query_string


def _serialize_sparql_bindings(bindings):
    """Build a SPARQL VALUES string to bind each KV pair in bindings to the query"""
    bindings_statements = []
    for binding_name, binding_value in bindings.items():
        bindings_statements.append(f"VALUES (?{binding_name}) {{ ({binding_value.n3()}) }} .")
    return ' '.join(bindings_statements)


def _build_sparql_anding_statement(object_list, predicate, programme_binding='programme'):
    """Build a SPARQL query fragment that matches all objects in object_list"""
    if not object_list:
        return ''
    comma_separated_sparql_tags = ', '.join([uri.n3() for uri in object_list])
    tag_filter_statement = f"?{programme_binding} {predicate.n3()} {comma_separated_sparql_tags} ."
    return tag_filter_statement


def _build_values_oring_statement(binding, object_list):
    """Build a SPARQL VALUES string to bind everything in object_list by logical OR"""
    if not object_list:
        return ''
    object_bindings = ' '.join([f"({sparql_binding.n3()})" for sparql_binding in object_list])
    return f"VALUES (?{binding}) {{ {object_bindings} }} ."


def _build_sort_query(sort_string):
    # TODO
    pass
